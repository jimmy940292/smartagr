from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd
import matplotlib.ticker as ticker

# figFolder = "fig/fishtank_20cm_dry_sand_M31_9am/lora/"
# logFolderName = "fishtank_20cm_dry_sand_M31_9am/"

figFolder = "fig/rock_40/lora/"
logFolderName = "rock/rock_40/"
senderLogFileName = "lora_send"
receiverLogFileName = "lora_recv"

prefix = "rock40_"

# distance = "D1B125T1_"
# distance = "D1B125T3_"
# distance = "D1B125T15_"

# distance = "D2B125T1_"
# distance = "D2B125T3_"
# distance = "D2B125T15_"

# distance = "D4B500T1_"
# distance = "D4B500T3_"
distance = "D4B500T15_"


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
        p.packetSize = int(line.split(",")[1])
        # p.packetSize = 100
        p.timeStamp = float(line.split(",")[2])
        sendPacket.append(p)

    # Read receiver log file:
    for line in receiverLogFile:
        if (line == ""):
            break
        p = PacketLog()
        p.seq = int(line.split(",")[0])
        p.packetSize = int(line.split(",")[1])
        # p.packetSize = 100
        p.timeStamp = float(line.split(",")[2])
        p.rssi = float(line.split(",")[3])
        p.snr = float(line.split(",")[4])
        receivePacket.append(p)

    # first_t = datetime.fromtimestamp(receivePacket[0].timeStamp)
    # last_t = datetime.fromtimestamp(
    #     receivePacket[len(receivePacket) - 1].timeStamp)
    # delta = (last_t - first_t).total_seconds() * 1000.0

    recvIndex = 0
    recvLen = len(receivePacket)
    
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
            
        if(recvIndex >= recvLen):
            break

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
        p.packetSize = int(line.split(",")[1])
        # p.packetSize = 100
        p.timeStamp = float(line.split(",")[2])
        sendPacket.append(p)

    # Read receiver log file:
    for line in receiverLogFile:
        if (line == ""):
            break
        p = PacketLog()
        p.seq = int(line.split(",")[0])
        p.packetSize = int(line.split(",")[1])
        # p.packetSize = 100
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
        print(recvIndex)
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




def draw_bar(senderLogFiles, receiverLogFiles):

    ThroughputList = []
    LatencyList = []
    packetLossList = []
    RssiList = []
    SnrList = []

    for i in range(len(senderLogFiles)):
        t, l, p, r, s = cal_metric(
            senderLogFiles[i], receiverLogFiles[i], False)
        # t, l, p, r, s = cal_10s_metric(senderLogFiles[i], receiverLogFiles[i], False)
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
    # labels.append("Avg")

    x = []
    for i in range(len(labels)):
        x.append(i)

    # Throughput
    ThroughputList = pd.DataFrame(ThroughputList)
    ThroughputList = ThroughputList.T

    # ThroughputList['Avg'] = (ThroughputList[0] + ThroughputList[1] + ThroughputList[2] + ThroughputList[3] + ThroughputList[4] + ThroughputList[5] ) / 6
    plot_throughput = sns.barplot(
        data=ThroughputList, palette=colors, width=width, errorbar=('ci', 95), errwidth=20)
    plt.xlabel("Run", fontsize=my_fontsize)
    plt.ylabel("Throughput (kbps)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + prefix+ distance + "throughput_runs_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + prefix+distance + "throughput_runs_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # # Latency
    LatencyList = pd.DataFrame(LatencyList)
    LatencyList = LatencyList.T
    # LatencyList['Avg'] = (LatencyList[0] + LatencyList[1] + LatencyList[2] + LatencyList[3] + LatencyList[4] + LatencyList[5] ) / 6
    plot_latency = sns.barplot(
        data=LatencyList, palette=colors, width=width, errorbar=('ci', 95), errwidth=20)
    plt.xlabel("Run", fontsize=my_fontsize)
    plt.ylabel("Latency (ms)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + prefix + distance + "latency_runs_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + prefix+distance + "latency_runs_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # Packet loss rate
    packetLossList = pd.DataFrame(packetLossList)
    packetLossList = packetLossList.T
    # packetLossList['Avg'] = (packetLossList[0] + packetLossList[1] + packetLossList[2] + packetLossList[3] + packetLossList[4] + packetLossList[5] ) / 6
    plot_packetloss = sns.barplot(
        data=packetLossList, palette=colors, width=width, errorbar=('ci', 95), errwidth=20)
    plt.xlabel("Run", fontsize=my_fontsize)
    plt.ylabel("Packet Loss Rate (%)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    # plt.ylim(0.0, 100.0)
    plt.savefig(figFolder + prefix+distance + "packetlossrate_runs_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + prefix + distance + "packetlossrate_runs_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # SNR
    SnrList = pd.DataFrame(SnrList)
    SnrList = SnrList.T
    # SnrList['Avg'] = (SnrList[0] + SnrList[1] + SnrList[2] + SnrList[3] + SnrList[4] + SnrList[5] ) / 6
    plot_snr = sns.barplot(data=SnrList, palette=colors,
                           width=width, errorbar=('ci', 95), errwidth=20)
    plt.xlabel("Run", fontsize=my_fontsize)
    plt.ylabel("SNR (dB)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + prefix+distance +"snr_runs_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + prefix + distance + "snr_runs_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # RSSI
    newRssiList = RssiList
    RssiList = pd.DataFrame(RssiList)
    RssiList = RssiList.T
    # RssiList['Avg'] = (RssiList[0] + RssiList[1] + RssiList[2] + RssiList[3] + RssiList[4] + RssiList[5] ) / 6
    plot_rssi = sns.barplot(data=RssiList, palette=colors,
                            width=width, errorbar=('ci', 95), errwidth=20)
    plt.xlabel("Run", fontsize=my_fontsize)
    plt.ylabel("RSSI (dBm)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    # plt.ylim(RssiList.min(), 0)
    plt.savefig(figFolder + prefix+distance +
                "rssi_runs_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + prefix+distance + "rssi_runs_lora.eps",
                dpi=300, bbox_inches="tight")
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
            s_file = open(logFolderName + distance + senderLogFileName +
                          "_" + str(i) + ".log", "r")
            r_file = open(logFolderName + distance + receiverLogFileName +
                          "_" + str(i) + ".log", "r")

            senderLogFiles.append(s_file)
            receiverLogFiles.append(r_file)

            # cal_avg_metric(s_file, r_file, True)
        # Bar
        # draw_avg_bar(senderLogFiles, receiverLogFiles)
        draw_bar(senderLogFiles, receiverLogFiles)

    else:
        # Open log files
        senderLogFile = open(logFolderName + senderLogFileName +
                             "_" + str(args.expNumber) + ".log", "r")
        receiverLogFile = open(
            logFolderName + receiverLogFileName + "_" + str(args.expNumber) + ".log", "r")
        # cal_avg_metric(senderLogFile, receiverLogFile, True)
        cal_10s_metric(senderLogFile, receiverLogFile, True)
