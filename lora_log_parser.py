from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd
import matplotlib.ticker as ticker


logFolderName = "results/D80_B20_S1_M29/"
senderLogFileName = "lora_send"
receiverLogFileName = "lora_recv"
figFolder = "fig/M29/D80/lora/"

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



def cal_avg_metric(senderLogFile, receiverLogFile, doprint = True):
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
        if(line == ""):
            break
        p = PacketLog()
        p.seq = int(line.split(",")[0])
        p.packetSize = int(line.split(",")[1])
        p.timeStamp = float(line.split(",")[2])
        sendPacket.append(p)
        
    # Read receiver log file:
    for line in receiverLogFile:
        if(line == ""):
            break
        p = PacketLog()
        p.seq = int(line.split(",")[0])
        p.packetSize = int(line.split(",")[1])
        p.timeStamp = float(line.split(",")[2])
        p.rssi = float(line.split(",")[3])
        p.snr = float(line.split(",")[4])
        receivePacket.append(p)
        
    
    
    recvIndex = 0
    for i in range(len(sendPacket)):
        # print("{} : {}".format(receivePacket[recvIndex].seq, sendPacket[i].seq))
        if(receivePacket[recvIndex].seq != sendPacket[i].seq):
            lostPacket += 1
            continue
        else:
            t1 = datetime.fromtimestamp(sendPacket[i].timeStamp)
            t2 = datetime.fromtimestamp(receivePacket[recvIndex].timeStamp + 2) # Add time
            delta = (t2 - t1).total_seconds() * 1000.0
            throughputList.append(receivePacket[recvIndex].packetSize * 8.0 / 1000.0/ delta *1000.0) # kbps
            latencyList.append(delta) # ms
            rssiList.append(receivePacket[recvIndex].rssi)
            snrList.append(receivePacket[recvIndex].snr)
            recvIndex += 1
            
            
    # Calculate average metrics
    avgThroughput = sum(throughputList) / len(throughputList)
    avgLatency = sum(latencyList) / len(latencyList)
    avgRssi = sum(rssiList) / len(rssiList)
    avgSnr = sum(snrList) / len(snrList)
    if(lostPacket > 0):
        packetLoss = lostPacket / len(throughputList) * 100.0
    else:
        packetLoss = 0.0
    

    if(doprint):
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

    recvIndex = 0
    for i in range(len(sendPacket)):
        # print("{} : {}".format(receivePacket[recvIndex].seq, sendPacket[i].seq))
        if (receivePacket[recvIndex].seq != sendPacket[i].seq):
            lostPacket += 1
            continue
        else:
            t1 = datetime.fromtimestamp(sendPacket[i].timeStamp)
            t2 = datetime.fromtimestamp(receivePacket[recvIndex].timeStamp + 2)
            delta = (t2 - t1).total_seconds() * 1000.0
            throughputList.append(
                receivePacket[recvIndex].packetSize * 8.0 / 1000.0 / delta * 1000.0)  # kbps
            latencyList.append(delta)  # ms
            rssiList.append(receivePacket[recvIndex].rssi)
            snrList.append(receivePacket[recvIndex].snr)
            recvIndex += 1

    senderLogFile.close()
    receiverLogFile.close()

    return throughputList, latencyList, lostPacket, rssiList, snrList


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

    recvIndex = 0
    for i in range(len(sendPacket)):
        # print("{} : {}".format(receivePacket[recvIndex].seq, sendPacket[i].seq))
        if (receivePacket[recvIndex].seq != sendPacket[i].seq):
            lostPacket += 1
            continue
        else:
            t1 = datetime.fromtimestamp(sendPacket[i].timeStamp)
            t2 = datetime.fromtimestamp(receivePacket[recvIndex].timeStamp + 2)
            delta = (t2 - t1).total_seconds() * 1000.0
            throughputList.append(
                receivePacket[recvIndex].packetSize * 8.0 / 1000.0 / delta * 1000.0)  # kbps
            latencyList.append(delta)  # ms
            rssiList.append(receivePacket[recvIndex].rssi)
            snrList.append(receivePacket[recvIndex].snr)
            recvIndex += 1
      
    # Calculate average metrics in 10s
    avgThroughput = []
    avgLatency = []
    avgRssi = []
    avgSnr = []
    packetLoss = []
    
    index = int(len(sendPacket) / 10)
    for i in range(index):
        avgThroughput.append(sum(throughputList[i*10:i*10+9]) / len(throughputList[i*10:i*10+9]))
        avgLatency.append(sum(latencyList[i*10:i*10+9]) / len(latencyList[i*10:i*10+9]))
        avgRssi.append(sum(rssiList[i*10:i*10+9]) / len(rssiList[i*10:i*10+9]))
        avgSnr.append(sum(snrList[i*10:i*10+9]) / len(snrList[i*10:i*10+9]))
        packetLoss.append((lostPacket / index) / len(throughputList[i*10:i*10+9]))

    senderLogFile.close()
    receiverLogFile.close()

    return avgThroughput, avgLatency, packetLoss, avgRssi, avgSnr
    
def draw_avg_bar(senderLogFiles, receiverLogFiles):

    avgThroughputList = []
    avgLatencyList = []
    packetLossList = []
    avgRssiList = []
    avgSnrList = []
    
    for i in range(len(senderLogFiles)):
        t, l, p, r, s = cal_avg_metric(senderLogFiles[i], receiverLogFiles[i], False)
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
    avgThroughputList = np.reshape(avgThroughputList, (1, len(avgThroughputList)))
    avgThroughputList = pd.DataFrame(avgThroughputList)
    plot_throughput = sns.barplot(data=avgThroughputList, palette=colors, width=width,errorbar=('ci', 95),errwidth=20)
    plt.xlabel("Run", fontsize=my_fontsize)
    plt.ylabel("Throughput (kbps)", fontsize=my_fontsize)
    plt.xticks(x,labels,fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + "throughput_bar.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "throughput_bar.eps", dpi=300, bbox_inches="tight")
    plt.clf()
    
    
    # Latency    
    avgLatencyList = np.array(avgLatencyList)
    avgLatencyList = np.reshape(avgLatencyList, (1, len(avgLatencyList)))
    avgLatencyList = pd.DataFrame(avgLatencyList)
    plot_latency = sns.barplot(data=avgLatencyList, palette=colors, width=width,errorbar=('ci', 95),errwidth=20)  
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
    plot_packetloss = sns.barplot(data=packetLossList, palette=colors, width=width,errorbar=('ci', 95),errwidth=20)
    plt.xlabel("Run", fontsize=my_fontsize)
    plt.ylabel("Packet loss rate (%)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.ylim(0.0, 100.0)
    plt.savefig(figFolder + "packetlossrate_bar.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "packetlossrate_bar.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    
    
    
    # SNR   
    avgSnrList = np.array(avgSnrList)
    avgSnrList = np.reshape(avgSnrList, (1, len(avgSnrList)))
    avgSnrList = pd.DataFrame(avgSnrList)
    plot_snr = sns.barplot(data=avgSnrList, palette=colors, width=width,errorbar=('ci', 95),errwidth=20)
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
    plot_rssi = sns.barplot(data=avgRssiList, palette=colors, width=width,errorbar=('ci', 95),errwidth=20)
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
    ThroughputList['Avg'] = (ThroughputList[0]+ ThroughputList[1] + ThroughputList[2] + ThroughputList[3] + ThroughputList[4] + ThroughputList[5] + ThroughputList[6] + ThroughputList[7] + ThroughputList[8] + ThroughputList[9] + ThroughputList[10] + ThroughputList[11]) / 12
    plot_throughput = sns.barplot(
        data=ThroughputList, palette=colors, width=width, errorbar=('ci', 95), errwidth=20)
    plt.xlabel("Run", fontsize=my_fontsize)
    plt.ylabel("Throughput (kbps)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + "throughput_bar.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "throughput_bar.eps", dpi=300, bbox_inches="tight")
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
    plt.savefig(figFolder + "latency_bar.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "latency_bar.eps", dpi=300, bbox_inches="tight")
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
    plt.ylabel("Packet loss rate (%)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    # plt.ylim(0.0, 100.0)
    plt.savefig(figFolder + "packetlossrate_bar.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "packetlossrate_bar.eps",
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
    plt.savefig(figFolder + "snr_bar.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "snr_bar.eps", dpi=300, bbox_inches="tight")
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
    plt.savefig(figFolder + "rssi_bar.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "rssi_bar.eps", dpi=300, bbox_inches="tight")
    plt.clf()


def draw_avg_line(senderLogFiles, receiverLogFiles):
    
    
    # Plot parameters
    
    colors = ["blue", "red", "green", 'purple', 'brown']
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    
    
    
    # 0
    t0, l0, p0, r0, s0 = cal_10s_metric(senderLogFiles[0], receiverLogFiles[0], False)
    
    # 1
    t1, l1, p1, r1, s1 = cal_10s_metric(senderLogFiles[1], receiverLogFiles[1], False)
    
    # 2
    t2, l2, p2, r2, s2 = cal_10s_metric(senderLogFiles[2], receiverLogFiles[2], False)
    
    # Throughput
    plt.plot(x, t0, color=colors[0], label="1", linestyle="--", marker=">", linewidth=10, markersize=80, markevery=1)
    plt.plot(x, t1, color=colors[1], label="2", linestyle="-", marker="o", linewidth=10, markersize=80, markevery=1)
    plt.plot(x, t2, color=colors[2], label="3", linestyle="-.", marker="v", linewidth=10, markersize=80, markevery=1)
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 11)
    plt.xlabel('Time (s)', fontsize=my_fontsize)
    plt.ylabel(f'Throughput (kbps)', fontsize=my_fontsize)
    plt.legend(loc="upper center", fancybox=False, labelspacing=0.05, handletextpad=0.5, ncol=3, borderpad=0.25,title="", framealpha=1, columnspacing=0.2, fontsize=my_fontsize, bbox_to_anchor=(0.5, 1.19))
    plt.tight_layout()
    plt.savefig(figFolder + "throughput_line.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "throughput_line.eps", dpi=300, bbox_inches="tight")
    plt.clf()
    
    # Latency
    plt.plot(x, l0, color=colors[0], label="1", linestyle="--", marker=">", linewidth=10, markersize=80, markevery=1)
    plt.plot(x, l1, color=colors[1], label="2", linestyle="-", marker="o", linewidth=10, markersize=80, markevery=1)
    plt.plot(x, l2, color=colors[2], label="3", linestyle="-.", marker="v", linewidth=10, markersize=80, markevery=1)
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 11)
    plt.xlabel('Time (s)', fontsize=my_fontsize)
    plt.ylabel(f'Latency (ms)', fontsize=my_fontsize)
    plt.legend(loc="upper center", fancybox=False, labelspacing=0.05, handletextpad=0.5, ncol=3, borderpad=0.25,title="", framealpha=1, columnspacing=0.2, fontsize=my_fontsize, bbox_to_anchor=(0.5, 1.19))
    plt.tight_layout()
    plt.savefig(figFolder + "latency_line.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "latency_line.eps", dpi=300, bbox_inches="tight")
    plt.clf()
    
    
    # Packet loss rate
    plt.plot(x, p0, color=colors[0], label="1", linestyle="--", marker=">", linewidth=10, markersize=80, markevery=1)
    plt.plot(x, p1, color=colors[1], label="2", linestyle="-", marker="o", linewidth=10, markersize=80, markevery=1)
    plt.plot(x, p2, color=colors[2], label="3", linestyle="-.", marker="v", linewidth=10, markersize=80, markevery=1)
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 11)
    plt.xlabel('Time (s)', fontsize=my_fontsize)
    plt.ylabel(f'Packet loss rate (%)', fontsize=my_fontsize)
    plt.legend(loc="upper center", fancybox=False, labelspacing=0.05, handletextpad=0.5, ncol=3, borderpad=0.25,title="", framealpha=1, columnspacing=0.2, fontsize=my_fontsize, bbox_to_anchor=(0.5, 1.19))
    plt.tight_layout()
    plt.savefig(figFolder + "packetlossrate_line.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "packetlossrate_line.eps", dpi=300, bbox_inches="tight")
    plt.clf()
    
    # SNR
    plt.plot(x, s0, color=colors[0], label="1", linestyle="--", marker=">", linewidth=10, markersize=80, markevery=1)
    plt.plot(x, s1, color=colors[1], label="2", linestyle="-", marker="o", linewidth=10, markersize=80, markevery=1)
    plt.plot(x, s2, color=colors[2], label="3", linestyle="-.", marker="v", linewidth=10, markersize=80, markevery=1)
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 11)
    plt.xlabel('Time (s)', fontsize=my_fontsize)
    plt.ylabel(f'SNR (dB)', fontsize=my_fontsize)
    plt.legend(loc="upper center", fancybox=False, labelspacing=0.05, handletextpad=0.5, ncol=3, borderpad=0.25,title="", framealpha=1, columnspacing=0.2, fontsize=my_fontsize, bbox_to_anchor=(0.5, 1.19))
    plt.tight_layout()
    plt.savefig(figFolder + "snr_line.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "snr_line.eps", dpi=300, bbox_inches="tight")
    plt.clf()
    
    # RSSI
    plt.plot(x, r0, color=colors[0], label="1", linestyle="--", marker=">", linewidth=10, markersize=80, markevery=1)
    plt.plot(x, r1, color=colors[1], label="2", linestyle="-", marker="o", linewidth=10, markersize=80, markevery=1)
    plt.plot(x, r2, color=colors[2], label="3", linestyle="-.", marker="v", linewidth=10, markersize=80, markevery=1)
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 11)
    plt.xlabel('Time (s)', fontsize=my_fontsize)
    plt.ylabel(f'RSSI (dBm)', fontsize=my_fontsize)
    plt.legend(loc="upper center", fancybox=False, labelspacing=0.05, handletextpad=0.5, ncol=3, borderpad=0.25,title="", framealpha=1, columnspacing=0.2, fontsize=my_fontsize, bbox_to_anchor=(0.5, 1.19))
    plt.tight_layout()
    plt.savefig(figFolder + "rssi_line.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "rssi_line.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    
    
    
    
if __name__ == "__main__":
    
    read_all_file = True
    
    
    # Args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--expNumber", type=int, default=0)
    args = parser.parse_args()
    
    
    if(read_all_file):
        senderLogFiles = []
        receiverLogFiles = []
        
        for i in range(args.expNumber + 1):
            s_file = open(logFolderName + senderLogFileName + "_" + str(i) + ".log", "r")
            r_file = open(logFolderName + receiverLogFileName + "_" + str(i) + ".log", "r")
            
            senderLogFiles.append(s_file)
            receiverLogFiles.append(r_file)
        
            # cal_avg_metric(s_file, r_file, True)
        # Bar
        # draw_avg_bar(senderLogFiles, receiverLogFiles)
        draw_bar(senderLogFiles, receiverLogFiles)
        
        
        # Line
        # draw_avg_line(senderLogFiles, receiverLogFiles)
    else:
        # Open log files
        senderLogFile = open(logFolderName + senderLogFileName + "_" + str(args.expNumber) + ".log", "r")
        receiverLogFile = open(logFolderName + receiverLogFileName + "_" + str(args.expNumber) + ".log", "r")
        # cal_avg_metric(senderLogFile, receiverLogFile, True)
        cal_10s_metric(senderLogFile, receiverLogFile, True)
            
            
    
    
    
    
    
            
            
            