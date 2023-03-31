from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd
import matplotlib.ticker as ticker

figFolder = "fig/fishtank_20cm_dry_sand_M31_9am/lora/"
logFolderName = "fishtank_20cm_dry_sand_M31_9am/"

# figFolder = "fig/M29/D160/lora/"
# logFolderName = "results/D160_B20_S1_M29/"
senderLogFileName = "lora_send"
receiverLogFileName = "lora_recv"

distance = "dry_sand_D20_"


# Parameters
my_fontsize = 110
my_figsize = (30, 22)
my_rotation = 45
tick_coe = 1
width = 0.6


class PacketLog():

    def __init__(self):
        self.seq = 0
        self.packetSize = 0
        self.timeStamp = 0
        self.rssi = 0
        self.snr = 0


def cal_avg_metric(senderLogFile, receiverLogFile, doprint=True):
    # Variable
    sendPacketNumber = 0
    lostPacket = 0
    sendPacket = []
    receivePacket = []
    throughputList = []
    latencyList = []
    rssiList = []
    snrList = []

    # Read sender log file
    for line in senderLogFile:
        if (line == ""):
            break
        p = PacketLog()
        p.seq = int(line.split(",")[0])
        p.packetSize = int(line.split(",")[1])
        p.timeStamp = float(line.split(",")[2])
        sendPacket.append(p)

    # Read receiver log file:
    for line in receiverLogFile:
        if (line == ""):
            break
        p = PacketLog()
        p.seq = int(line.split(",")[0])
        p.packetSize = int(line.split(",")[1])
        p.timeStamp = float(line.split(",")[2])
        p.rssi = float(line.split(",")[3])
        p.snr = float(line.split(",")[4])
        receivePacket.append(p)

    first_t = datetime.fromtimestamp(receivePacket[0].timeStamp)
    last_t = datetime.fromtimestamp(
        receivePacket[len(receivePacket) - 1].timeStamp)
    delta = (last_t - first_t).total_seconds() * 1000.0

    recvIndex = 0
    for i in range(len(sendPacket)):
        # print("{} : {}".format(receivePacket[recvIndex].seq, sendPacket[i].seq))
        if (receivePacket[recvIndex].seq != sendPacket[i].seq):
            lostPacket += 1
            continue
        else:
            # t1 = datetime.fromtimestamp(sendPacket[i].timeStamp)
            # t2 = datetime.fromtimestamp(receivePacket[recvIndex].timeStamp + 2) # Add time
            # delta = (t2 - t1).total_seconds() * 1000.0
            # throughputList.append(receivePacket[recvIndex].packetSize * 8.0 / 1000.0/ delta *1000.0) # kbps
            throughputList.append(
                receivePacket[recvIndex].packetSize * 8.0 / 1000.0)
            latencyList.append(delta)  # ms
            rssiList.append(receivePacket[recvIndex].rssi)
            snrList.append(receivePacket[recvIndex].snr)
            recvIndex += 1

    # Calculate average metrics
    avgThroughput = sum(throughputList) / 10.0
    avgLatency = sum(latencyList) / len(latencyList)
    avgRssi = sum(rssiList) / len(rssiList)
    avgSnr = sum(snrList) / len(snrList)
    if (lostPacket > 0):
        packetLoss = lostPacket / len(throughputList) * 100.0
    else:
        packetLoss = 0.0

    if (doprint):
        print("Avg Throughput: {} kbps".format(avgThroughput))
        print("Avg Latency: {} ms".format(avgLatency))
        print("Packet Loss Rate: {} %".format(packetLoss))
        print("Avg RSSI: {}".format(avgRssi))
        print("Avg SNR: {}".format(avgSnr))
        print()

    senderLogFile.close()
    receiverLogFile.close()

    return avgThroughput, avgLatency, packetLoss, avgRssi, avgSnr


def cal_metric(senderLogFile, receiverLogFile, doprint=True):
    # Variable
    sendPacketNumber = 0
    lostPacket = 0
    sendPacket = []
    receivePacket = []
    throughputList = []
    latencyList = []
    rssiList = []
    snrList = []

    # Read sender log file
    for line in senderLogFile:
        if (line == ""):
            break
        p = PacketLog()
        p.seq = int(line.split(",")[0])
        # p.packetSize = int(line.split(",")[1])
        p.packetSize = 100
        p.timeStamp = float(line.split(",")[2])
        sendPacket.append(p)

    # Read receiver log file:
    for line in receiverLogFile:
        if (line == ""):
            break
        p = PacketLog()
        p.seq = int(line.split(",")[0])
        # p.packetSize = int(line.split(",")[1])
        p.packetSize = 100
        p.timeStamp = float(line.split(",")[2])
        p.rssi = float(line.split(",")[3])
        p.snr = float(line.split(",")[4])
        receivePacket.append(p)

    # first_t = datetime.fromtimestamp(receivePacket[0].timeStamp)
    # last_t = datetime.fromtimestamp(
    #     receivePacket[len(receivePacket) - 1].timeStamp)
    # delta = (last_t - first_t).total_seconds() * 1000.0

    recvIndex = 0
    for i in range(len(sendPacket)):
        # print("{} : {}".format(receivePacket[recvIndex].seq, sendPacket[i].seq))
        if (receivePacket[recvIndex].seq != sendPacket[i].seq):
            lostPacket += 1
            continue
        else:
            t1 = datetime.fromtimestamp(sendPacket[i].timeStamp)
            t2 = datetime.fromtimestamp(receivePacket[recvIndex].timeStamp)
            delta = (t2 - t1).total_seconds() * 1000.0
            throughputList.append(
                receivePacket[recvIndex].packetSize * 8.0 / 1000.0)  # kbps
            latencyList.append(delta)  # ms
            rssiList.append(receivePacket[recvIndex].rssi)
            snrList.append(receivePacket[recvIndex].snr)
            recvIndex += 1

    senderLogFile.close()
    receiverLogFile.close()

    return sum(throughputList) / 10.0, latencyList, lostPacket, rssiList, snrList


def cal_10s_metric(senderLogFile, receiverLogFile, doprint=True):
    # Variable
    sendPacketNumber = 0
    lostPacket = 0
    sendPacket = []
    receivePacket = []
    throughputList = []
    latencyList = []
    rssiList = []
    snrList = []

    # Read sender log file
    for line in senderLogFile:
        if (line == ""):
            break
        p = PacketLog()
        p.seq = int(line.split(",")[0])
        # p.packetSize = int(line.split(",")[1])
        p.packetSize = 100
        p.timeStamp = float(line.split(",")[2])
        sendPacket.append(p)

    # Read receiver log file:
    for line in receiverLogFile:
        if (line == ""):
            break
        p = PacketLog()
        p.seq = int(line.split(",")[0])
        # p.packetSize = int(line.split(",")[1])
        p.packetSize = 100
        p.timeStamp = float(line.split(",")[2])
        p.rssi = float(line.split(",")[3])
        p.snr = float(line.split(",")[4])
        receivePacket.append(p)
        
     # Calculate average metrics in 10s
    avgThroughput = []
    avgLatency = []
    avgRssi = []
    avgSnr = []
    packetLoss = []

    first_t = datetime.fromtimestamp(receivePacket[0].timeStamp)
    # last_t = datetime.fromtimestamp(
    #     receivePacket[len(receivePacket) - 1].timeStamp)
    # delta = (last_t - first_t).total_seconds() * 1000.0

    recvIndex = 0
    index = int(len(sendPacket) / 10)
    
    loss_list = []
    t = receivePacket[0].packetSize
    for i in range(len(receivePacket)):
        if ((datetime.fromtimestamp(receivePacket[i].timeStamp) - first_t).total_seconds() < 1.0):
            t += (receivePacket[i].packetSize * 8.0 / 1000.0)
        else:
            avgThroughput.append(t)
            t = receivePacket[i].packetSize
            first_t = datetime.fromtimestamp(receivePacket[i].timeStamp)     
    avgThroughput.append(t)
    
        
    
    
    for i in range(len(sendPacket)):
        # print("{} : {}".format(receivePacket[recvIndex].seq, sendPacket[i].seq))
        if (receivePacket[recvIndex].seq != sendPacket[i].seq):
            latencyList.append(0)  # ms
            rssiList.append(0)
            snrList.append(0)
            lostPacket += 1
        else:
            t1 = datetime.fromtimestamp(sendPacket[i].timeStamp)
            t2 = datetime.fromtimestamp(receivePacket[recvIndex].timeStamp)
            delta = (t2 - t1).total_seconds() * 1000.0
            # throughputList.append(
            #     receivePacket[recvIndex].packetSize * 8.0 / 1000.0 / delta * 1000.0)  # kbps
            # throughputList.append(
            #     receivePacket[recvIndex].packetSize * 8.0 / 1000.0)  # kbps
            latencyList.append(delta)  # ms
            rssiList.append(receivePacket[recvIndex].rssi)
            snrList.append(receivePacket[recvIndex].snr)
            recvIndex += 1
        if (i % index == 9):
            loss_list.append(lostPacket)
            lostPacket = 0
        
            
    # print("{} : {}".format(len(latencyList), len(sendPacket)))
    # for i in range(len(latencyList)):
    #     print(latencyList[i])
    l =len(avgThroughput)
    for i in range(l, 10):
        avgThroughput.append(t)

    for i in range(index):
        # avgThroughput.append(
        #     sum(throughputList[i*10:i*10+9]) / len(throughputList[i*10:i*10+9]) * 100.0)
        # avgThroughput.append(sum(throughputList[i*10:i*10+9]) * 10)
        sumLatency = 0
        validLatency = 0
        for j in range(i*10, (i+1)*10):
            if(latencyList[j] != 0):
                validLatency += 1
                sumLatency += latencyList[j]
        if(validLatency == 0):
            avgLatency.append(0)
        else:
            avgLatency.append(sumLatency / validLatency)

        sumRssi = 0
        validRssi = 0
        for j in range(i*10, (i+1)*10):
            if(rssiList[j] != 0):
                validRssi += 1
                sumRssi += rssiList[j]
        if(validRssi == 0):
            avgRssi.append(0)
        else:
            avgRssi.append(sumRssi / validRssi)

        sumSnr = 0
        validSnr = 0
        for j in range(i*10, (i+1)*10):
            if(snrList[j] != 0):
                validSnr += 1
                sumSnr += snrList[j]
        if(validSnr == 0):
            avgSnr.append(0)
        else:
            avgSnr.append(sumSnr / validSnr)
        packetLoss.append((loss_list[i]) / len(sendPacket[i*10:(i+1)*10]) * 100.0)
        # if (len(latencyList[i*10:(i+1)*10]) > 0):
        #     avgLatency.append(
        #     sum(latencyList[i*10:(i+1)*10]) / len(latencyList[i*10:(i+1)*10]))
        # else:
        #     avgLatency.append(0)
        # if (len(rssiList[i*10:(i+1)*10]) > 0):
        #     avgRssi.append(sum(rssiList[i*10:(i+1)*10]) / len(rssiList[i*10:(i+1)*10]))
        # else:
        #     avgRssi.append(0)
        # if (len(snrList[i*10:(i+1)*10]) > 0):
        #     avgSnr.append(sum(snrList[i*10:(i+1)*10]) / len(snrList[i*10:(i+1)*10]))
        # else:
        #     avgSnr.append(0)
        # packetLoss.append(
        #     (loss_list[i]) / len(sendPacket[i*10:(i+1)*10]) * 100.0)

    senderLogFile.close()
    receiverLogFile.close()

    return np.array(avgThroughput), np.array(avgLatency), np.array(packetLoss), np.array(avgRssi), np.array(avgSnr)


def draw_avg_bar(senderLogFiles, receiverLogFiles):

    avgThroughputList = []
    avgLatencyList = []
    packetLossList = []
    avgRssiList = []
    avgSnrList = []

    for i in range(len(senderLogFiles)):
        t, l, p, r, s = cal_avg_metric(
            senderLogFiles[i], receiverLogFiles[i], False)
        avgThroughputList.append(t)
        avgLatencyList.append(l)
        packetLossList.append(p)
        avgRssiList.append(r)
        avgSnrList.append(s)

    # Add average into list
    avgThroughputList.append(sum(avgThroughputList)/len(avgThroughputList))
    avgLatencyList.append(sum(avgLatencyList)/len(avgLatencyList))
    packetLossList.append(sum(packetLossList)/len(packetLossList))
    avgRssiList.append(sum(avgRssiList)/len(avgRssiList))
    avgSnrList.append(sum(avgSnrList)/len(avgSnrList))

    # Draw Fig
    colors = ["blue", "red", "green", 'purple', 'brown']
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    # Label
    labels = []
    for i in range(len(avgThroughputList) - 1):
        labels.append(str(i))
    labels.append("Avg")

    x = []
    for i in range(len(labels)):
        x.append(i)

    # Throughput
    avgThroughputList = np.array(avgThroughputList)
    avgThroughputList = np.reshape(
        avgThroughputList, (1, len(avgThroughputList)))
    avgThroughputList = pd.DataFrame(avgThroughputList)
    plot_throughput = sns.barplot(
        data=avgThroughputList, palette=colors, width=width, errorbar=('ci', 95), errwidth=20)
    plt.xlabel("Run", fontsize=my_fontsize)
    plt.ylabel("Throughput (kbps)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + "throughput_bar.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "throughput_bar.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    # Latency
    avgLatencyList = np.array(avgLatencyList)
    avgLatencyList = np.reshape(avgLatencyList, (1, len(avgLatencyList)))
    avgLatencyList = pd.DataFrame(avgLatencyList)
    plot_latency = sns.barplot(
        data=avgLatencyList, palette=colors, width=width, errorbar=('ci', 95), errwidth=20)
    plt.xlabel("Run", fontsize=my_fontsize)
    plt.ylabel("Latency (ms)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + "latency_bar.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "latency_bar.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    # Packet loss rate
    packetLossList = np.array(packetLossList)
    newpacketloss = packetLossList
    packetLossList = np.reshape(packetLossList, (1, len(packetLossList)))
    packetLossList = pd.DataFrame(packetLossList)
    plot_packetloss = sns.barplot(
        data=packetLossList, palette=colors, width=width, errorbar=('ci', 95), errwidth=20)
    plt.xlabel("Run", fontsize=my_fontsize)
    plt.ylabel("Packet loss rate (%)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.ylim(0.0, 100.0)
    plt.savefig(figFolder + "packetlossrate_bar.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "packetlossrate_bar.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # SNR
    avgSnrList = np.array(avgSnrList)
    avgSnrList = np.reshape(avgSnrList, (1, len(avgSnrList)))
    avgSnrList = pd.DataFrame(avgSnrList)
    plot_snr = sns.barplot(data=avgSnrList, palette=colors,
                           width=width, errorbar=('ci', 95), errwidth=20)
    plt.xlabel("Run", fontsize=my_fontsize)
    plt.ylabel("SNR (dB)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + "snr_bar.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "snr_bar.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    # RSSI
    avgRssiList = np.array(avgRssiList)
    newRssiList = avgRssiList
    avgRssiList = np.reshape(avgRssiList, (1, len(avgRssiList)))
    avgRssiList = pd.DataFrame(avgRssiList)
    plot_rssi = sns.barplot(data=avgRssiList, palette=colors,
                            width=width, errorbar=('ci', 95), errwidth=20)
    plt.xlabel("Run", fontsize=my_fontsize)
    plt.ylabel("RSSI (dBm)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.ylim(min(newRssiList), 0)
    plt.savefig(figFolder + "rssi_bar.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "rssi_bar.eps", dpi=300, bbox_inches="tight")
    plt.clf()


def draw_bar(senderLogFiles, receiverLogFiles):

    ThroughputList = []
    LatencyList = []
    packetLossList = []
    RssiList = []
    SnrList = []

    for i in range(len(senderLogFiles)):
        t, l, p, r, s = cal_metric(
            senderLogFiles[i], receiverLogFiles[i], False)
        ThroughputList.append(t)
        LatencyList.append(l)
        packetLossList.append(p)
        RssiList.append(r)
        SnrList.append(s)

    # Draw Fig
    colors = ["blue", "red", "green", 'purple', 'brown']
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    # Label
    labels = []
    for i in range(len(ThroughputList)):
        labels.append(str(i))
    labels.append("Avg")

    x = []
    for i in range(len(labels)):
        x.append(i)

    # Throughput
    ThroughputList = pd.DataFrame(ThroughputList)
    ThroughputList = ThroughputList.T
    # ThroughputList['Avg'] = (ThroughputList[0]+ ThroughputList[1] + ThroughputList[2]) / 3
    ThroughputList['Avg'] = (ThroughputList[0] + ThroughputList[1] + ThroughputList[2] + ThroughputList[3] + ThroughputList[4] + ThroughputList[5] +
                             ThroughputList[6] + ThroughputList[7] + ThroughputList[8] + ThroughputList[9] + ThroughputList[10] + ThroughputList[11]) / 12
    plot_throughput = sns.barplot(
        data=ThroughputList, palette=colors, width=width, errorbar=('ci', 95), errwidth=20)
    plt.xlabel("Run", fontsize=my_fontsize)
    plt.ylabel("Throughput (kbps)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + distance +"throughput_runs_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + distance + "throughput_runs_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # # Latency
    LatencyList = pd.DataFrame(LatencyList)
    LatencyList = LatencyList.T
    # LatencyList['Avg'] = (LatencyList[0] + LatencyList[1] + LatencyList[2]) / 3
    LatencyList['Avg'] = (LatencyList[0] + LatencyList[1] + LatencyList[2] + LatencyList[3] + LatencyList[4] + LatencyList[5] +
                          LatencyList[6] + LatencyList[7] + LatencyList[8] + LatencyList[9] + LatencyList[10] + LatencyList[11]) / 12
    plot_latency = sns.barplot(
        data=LatencyList, palette=colors, width=width, errorbar=('ci', 95), errwidth=20)
    plt.xlabel("Run", fontsize=my_fontsize)
    plt.ylabel("Latency (ms)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + distance + "latency_runs_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + distance + "latency_runs_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # Packet loss rate
    packetLossList = pd.DataFrame(packetLossList)
    packetLossList = packetLossList.T
    # packetLossList['Avg'] = (packetLossList[0] + packetLossList[1] + packetLossList[2]) / 3
    packetLossList['Avg'] = (packetLossList[0] + packetLossList[1] + packetLossList[2] + packetLossList[3] + packetLossList[4] + packetLossList[5] +
                             packetLossList[6] + packetLossList[7] + packetLossList[8] + packetLossList[9] + packetLossList[10] + packetLossList[11]) / 12
    plot_packetloss = sns.barplot(
        data=packetLossList, palette=colors, width=width, errorbar=('ci', 95), errwidth=20)
    plt.xlabel("Run", fontsize=my_fontsize)
    plt.ylabel("Packet Loss Rate (%)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    # plt.ylim(0.0, 100.0)
    plt.savefig(figFolder + distance +"packetlossrate_runs_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + distance + "packetlossrate_runs_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # SNR
    SnrList = pd.DataFrame(SnrList)
    SnrList = SnrList.T
    # SnrList['Avg'] = (SnrList[0] + SnrList[1] + SnrList[2]) / 3
    SnrList['Avg'] = (SnrList[0] + SnrList[1] + SnrList[2] + SnrList[3] + SnrList[4] + SnrList[5] +
                      SnrList[6] + SnrList[7] + SnrList[8] + SnrList[9] + SnrList[10] + SnrList[11]) / 12
    plot_snr = sns.barplot(data=SnrList, palette=colors,
                           width=width, errorbar=('ci', 95), errwidth=20)
    plt.xlabel("Run", fontsize=my_fontsize)
    plt.ylabel("SNR (dB)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + distance +"snr_runs_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + distance + "snr_runs_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # RSSI
    newRssiList = RssiList
    RssiList = pd.DataFrame(RssiList)
    RssiList = RssiList.T
    # RssiList['Avg'] = (RssiList[0] + RssiList[1] + RssiList[2]) / 3
    RssiList['Avg'] = (RssiList[0] + RssiList[1] + RssiList[2] + RssiList[3] + RssiList[4] + RssiList[5] +
                       RssiList[6] + RssiList[7] + RssiList[8] + RssiList[9] + RssiList[10] + RssiList[11]) / 12
    plot_rssi = sns.barplot(data=RssiList, palette=colors,
                            width=width, errorbar=('ci', 95), errwidth=20)
    plt.xlabel("Run", fontsize=my_fontsize)
    plt.ylabel("RSSI (dBm)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    # plt.ylim(RssiList.min(), 0)
    plt.savefig(figFolder +distance + "rssi_runs_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + distance + "rssi_runs_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()


def draw_avg_line(senderLogFiles, receiverLogFiles):
    # Plot parameters

    # colors = ["blue", "red", "green", 'purple', 'brown']
    colors = ["blue", "red", "green", 'purple', 'brown', 'orange',
              'pink', 'gray', 'olive', 'cyan', 'darkblue', 'black']
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    # 0
    t0, l0, p0, r0, s0 = cal_10s_metric(
        senderLogFiles[0], receiverLogFiles[0], False)

    # 1
    t1, l1, p1, r1, s1 = cal_10s_metric(
        senderLogFiles[1], receiverLogFiles[1], False)

    # 2
    t2, l2, p2, r2, s2 = cal_10s_metric(
        senderLogFiles[2], receiverLogFiles[2], False)

    # 3
    t3, l3, p3, r3, s3 = cal_10s_metric(
        senderLogFiles[3], receiverLogFiles[3], False)

    # # 4
    t4, l4, p4, r4, s4 = cal_10s_metric(
        senderLogFiles[4], receiverLogFiles[4], False)

    # # 5
    t5, l5, p5, r5, s5 = cal_10s_metric(
        senderLogFiles[5], receiverLogFiles[5], False)

    # # 6
    t6, l6, p6, r6, s6 = cal_10s_metric(
        senderLogFiles[6], receiverLogFiles[6], False)

    # # 7
    t7, l7, p7, r7, s7 = cal_10s_metric(
        senderLogFiles[7], receiverLogFiles[7], False)

    # # 8
    t8, l8, p8, r8, s8 = cal_10s_metric(
        senderLogFiles[8], receiverLogFiles[8], False)

    # # 9
    t9, l9, p9, r9, s9 = cal_10s_metric(
        senderLogFiles[9], receiverLogFiles[9], False)

    # # 10
    t10, l10, p10, r10, s10 = cal_10s_metric(
        senderLogFiles[10], receiverLogFiles[10], False)

    # # 11
    t11, l11, p11, r11, s11 = cal_10s_metric(
        senderLogFiles[11], receiverLogFiles[11], False)

    # Throughput
    mask = t0 != 0
    plt.plot(x[mask], t0[mask], color=colors[0], label="1", linestyle="--",
             marker=">", linewidth=10, markersize=80, markevery=1)
    mask = t8 != 0
    plt.plot(x[mask], t8[mask], color=colors[8], label="9", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    # plt.plot(x[mask], t1, color=colors[1], label="1", linestyle="-",
    #          marker="o", linewidth=10, markersize=80, markevery=1)
    
    mask = t2 != 0
    plt.plot(x[mask], t2[mask], color=colors[2], label="3", linestyle="-",
             marker="o", linewidth=10, markersize=80, markevery=1)
    mask = t10 != 0
    plt.plot(x[mask], t10[mask], color=colors[10], label="11", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    # plt.plot(x[mask], t3, color=colors[3], label="3", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    mask = t4 != 4
    plt.plot(x[mask], t4[mask], color=colors[4], label="5", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    # plt.plot(x[mask], t5, color=colors[5], label="5", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    mask = t6 != 0
    plt.plot(x[mask], t6[mask], color=colors[6], label="7", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    # plt.plot(x[mask], t7, color=colors[7], label="7", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    
    # plt.plot(x[mask], t9, color=colors[9], label="9", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    
    # plt.plot(x[mask], t11, color=colors[11], label="11", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 11)
    plt.xlabel('Time (s)', fontsize=my_fontsize)
    plt.ylabel(f'Throughput (kbps)', fontsize=my_fontsize)
    plt.legend(loc="upper center", fancybox=False, labelspacing=0.05, handletextpad=0.5, ncol=4, borderpad=0.25,
               title="", framealpha=1, columnspacing=0.2, fontsize=my_fontsize, bbox_to_anchor=(0.5, 1.35))
    plt.tight_layout()
    plt.savefig(figFolder + distance + "throughput_time_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + distance + "throughput_time_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # Latency
    mask = l0 != 0
    plt.plot(x[mask], l0[mask], color=colors[0], label="1", linestyle="--",
             marker=">", linewidth=10, markersize=80, markevery=1)
    mask = l8 != 0
    plt.plot(x[mask], l8[mask], color=colors[8], label="9", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    mask = l2 != 0
    plt.plot(x[mask], l2[mask], color=colors[2], label="3", linestyle="-",
             marker="o", linewidth=10, markersize=80, markevery=1)
    mask = l10 != 0
    plt.plot(x[mask], l10[mask], color=colors[10], label="11", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    mask = l4 != 0
    plt.plot(x[mask], l4[mask], color=colors[4], label="5", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    # plt.plot(x[mask], l1, color=colors[1], label="2", linestyle="-",
    #          marker="o", linewidth=10, markersize=80, markevery=1)
    
    # plt.plot(x[mask], l3, color=colors[3], label="3", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    
    # plt.plot(x[mask], l5, color=colors[5], label="5", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    mask = l6 != 0
    plt.plot(x[mask], l6[mask], color=colors[6], label="6", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    # plt.plot(x[mask], l7, color=colors[7], label="7", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    
    # plt.plot(x[mask], l9, color=colors[9], label="9", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    
    # plt.plot(x[mask], l11, color=colors[11], label="11", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 11)
    plt.xlabel('Time (s)', fontsize=my_fontsize)
    plt.ylabel(f'Latency (ms)', fontsize=my_fontsize)
    plt.legend(loc="upper center", fancybox=False, labelspacing=0.05, handletextpad=0.5, ncol=4, borderpad=0.25,
               title="", framealpha=1, columnspacing=0.2, fontsize=my_fontsize, bbox_to_anchor=(0.5, 1.35))
    plt.tight_layout()
    plt.savefig(figFolder +distance + "latency_time_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + distance + "latency_time_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # Packet loss rate
    plt.plot(x, p0, color=colors[0], label="1", linestyle="--",
             marker=">", linewidth=10, markersize=80, markevery=1)
    plt.plot(x, p8, color=colors[8], label="9", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    
    # plt.plot(x, p1, color=colors[1], label="2", linestyle="-",
    #          marker="o", linewidth=10, markersize=80, markevery=1)
    plt.plot(x, p2, color=colors[2], label="3", linestyle="-",
             marker="o", linewidth=10, markersize=80, markevery=1)
    plt.plot(x, p10, color=colors[10], label="11", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    # plt.plot(x, p3, color=colors[3], label="4", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    plt.plot(x, p4, color=colors[4], label="5", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    # plt.plot(x, p5, color=colors[5], label="6", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    plt.plot(x, p6, color=colors[6], label="7", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    # plt.plot(x, p7, color=colors[7], label="8", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    
    # plt.plot(x, p9, color=colors[9], label="1", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    
    # plt.plot(x, p11, color=colors[11], label="12", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 11)
    plt.xlabel('Time (s)', fontsize=my_fontsize)
    plt.ylabel(f'Packet Loss Rate (%)', fontsize=my_fontsize)
    plt.legend(loc="upper center", fancybox=False, labelspacing=0.05, handletextpad=0.5, ncol=4, borderpad=0.25,
               title="", framealpha=1, columnspacing=0.2, fontsize=my_fontsize, bbox_to_anchor=(0.5, 1.35))
    plt.tight_layout()
    plt.savefig(figFolder + distance + "packetlossrate_time_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + distance + "packetlossrate_time_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # SNR
    mask = s0 != 0
    plt.plot(x[mask], s0[mask], color=colors[0], label="1", linestyle="--",
             marker=">", linewidth=10, markersize=80, markevery=1)
    mask = s8 != 0
    plt.plot(x[mask], s8[mask], color=colors[8], label="9", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    # plt.plot(x[mask], s1, color=colors[1], label="2", linestyle="-",
    #          marker="o", linewidth=10, markersize=80, markevery=1)
    mask = s2 != 0
    plt.plot(x[mask], s2[mask], color=colors[2], label="3", linestyle="-",
             marker="o", linewidth=10, markersize=80, markevery=1)
    mask = s10 != 0
    plt.plot(x[mask], s10[mask], color=colors[10], label="11", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    # plt.plot(x[mask], s3, color=colors[3], label="4", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    mask = s4 != 0
    plt.plot(x[mask], s4[mask], color=colors[4], label="5", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    # plt.plot(x[mask], s5, color=colors[5], label="6", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    mask = s6 != 0
    plt.plot(x[mask], s6[mask], color=colors[6], label="7", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    # plt.plot(x[mask], s7, color=colors[7], label="8", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    
    # plt.plot(x[mask], s9, color=colors[9], label="10", linestyle="-.",
            #  marker="v", linewidth=10, markersize=80, markevery=1)
    
    # plt.plot(x[mask], s11, color=colors[11], label="12", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 11)
    plt.xlabel('Time (s)', fontsize=my_fontsize)
    plt.ylabel(f'SNR (dB)', fontsize=my_fontsize)
    plt.legend(loc="upper center", fancybox=False, labelspacing=0.05, handletextpad=0.5, ncol=4, borderpad=0.25,
               title="", framealpha=1, columnspacing=0.2, fontsize=my_fontsize, bbox_to_anchor=(0.5, 1.35))
    plt.tight_layout()
    plt.savefig(figFolder + distance +"snr_time_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + distance + "snr_time_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    mask = r0 != 0
    # RSSI
    plt.plot(x[mask], r0[mask], color=colors[0], label="1", linestyle="--",
             marker=">", linewidth=10, markersize=80, markevery=1)
    mask = r8 != 0
    plt.plot(x[mask], r8[mask], color=colors[8], label="9", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    # plt.plot(x[mask], r1, color=colors[1], label="2", linestyle="-",
    #          marker="o", linewidth=10, markersize=80, markevery=1)
    mask = r2 != 0
    plt.plot(x[mask], r2[mask], color=colors[2], label="3", linestyle="-",
             marker="o", linewidth=10, markersize=80, markevery=1)
    mask = r10 != 0
    plt.plot(x[mask], r10[mask], color=colors[10], label="11", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    # plt.plot(x[mask], r3, color=colors[3], label="4", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    mask = r4 != 0
    plt.plot(x[mask], r4[mask], color=colors[4], label="5", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    # plt.plot(x[mask], r5, color=colors[5], label="6", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    mask = r6 != 0
    plt.plot(x[mask], r6[mask], color=colors[6], label="7", linestyle="-.",
             marker="v", linewidth=10, markersize=80, markevery=1)
    # plt.plot(x[mask], r7, color=colors[7], label="8", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    
    # plt.plot(x[mask], r9, color=colors[9], label="10", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    
    # plt.plot(x[mask], r11, color=colors[11], label="12", linestyle="-.",
    #          marker="v", linewidth=10, markersize=80, markevery=1)
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 11)
    plt.xlabel('Time (s)', fontsize=my_fontsize)
    plt.ylabel(f'RSSI (dBm)', fontsize=my_fontsize)
    plt.legend(loc="upper center", fancybox=False, labelspacing=0.05, handletextpad=0.5, ncol=4, borderpad=0.25,
               title="", framealpha=1, columnspacing=0.2, fontsize=my_fontsize, bbox_to_anchor=(0.5, 1.35))
    plt.tight_layout()
    plt.savefig(figFolder + distance +"rssi_time_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + distance +"rssi_time_lora.eps", dpi=300, bbox_inches="tight")
    plt.clf()


if __name__ == "__main__":

    read_all_file = True

    # Args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--expNumber", type=int, default=0)
    args = parser.parse_args()

    if (read_all_file):
        senderLogFiles = []
        receiverLogFiles = []

        for i in range(args.expNumber + 1):
            s_file = open(logFolderName + senderLogFileName +
                          "_" + str(i) + ".log", "r")
            r_file = open(logFolderName + receiverLogFileName +
                          "_" + str(i) + ".log", "r")

            senderLogFiles.append(s_file)
            receiverLogFiles.append(r_file)

            # cal_avg_metric(s_file, r_file, True)
        # Bar
        # draw_avg_bar(senderLogFiles, receiverLogFiles)
        # draw_bar(senderLogFiles, receiverLogFiles)

        # Line
        draw_avg_line(senderLogFiles, receiverLogFiles)
    else:
        # Open log files
        senderLogFile = open(logFolderName + senderLogFileName +
                             "_" + str(args.expNumber) + ".log", "r")
        receiverLogFile = open(
            logFolderName + receiverLogFileName + "_" + str(args.expNumber) + ".log", "r")
        # cal_avg_metric(senderLogFile, receiverLogFile, True)
        cal_10s_metric(senderLogFile, receiverLogFile, True)
