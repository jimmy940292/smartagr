from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd
import matplotlib.ticker as ticker

logFolderName1 = "rock/rock_20/D4B500T15_"
logFolderName2 = "rock/rock_30/D4B500T15_"
logFolderName3 = "rock/rock_40/D4B500T15_"
senderLogFileName = "lora_send"
receiverLogFileName = "lora_recv"
figFolder = "fig/rock/lora/"
compare = "rock_"

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

        if (recvIndex >= recvLen):
            break

    senderLogFile.close()
    receiverLogFile.close()

    return sum(throughputList) / 10.0, latencyList, lostPacket, rssiList, snrList


def draw_compare_line(expNumber):
    
    # 1
    ThroughputList1 = []
    LatencyList1 = []
    packetLossList1 = []
    RssiList1 = []
    SnrList1 = []
    for i in range(expNumber + 1):
        t, l, p, r, s = cal_metric(open(logFolderName1 + senderLogFileName + "_" + str(
            i) + ".log", "r"), open(logFolderName1 + receiverLogFileName + "_" + str(i) + ".log", "r"))

        ThroughputList1.append(t)
        LatencyList1.append(l)
        packetLossList1.append(p)
        RssiList1.append(r)
        SnrList1.append(s)
        
    print(ThroughputList1)
    print(LatencyList1)
        
    ThroughputList1 = pd.DataFrame(ThroughputList1)
    ThroughputList1 = ThroughputList1.T


  
    LatencyList1 = pd.DataFrame(LatencyList1)
    LatencyList1 = LatencyList1.T

    
    packetLossList1 = pd.DataFrame(packetLossList1)
    packetLossList1 = packetLossList1.T

  
    RssiList1 = pd.DataFrame(RssiList1)
    RssiList1 = RssiList1.T

    
    SnrList1 = pd.DataFrame(SnrList1)
    SnrList1 = SnrList1.T
 
    
    # 2
    ThroughputList2 = []
    LatencyList2 = []
    packetLossList2 = []
    RssiList2 = []
    SnrList2 = []
    for i in range(expNumber + 1):
        t, l, p, r, s = cal_metric(open(logFolderName2 + senderLogFileName + "_" + str(
            i) + ".log", "r"), open(logFolderName2 + receiverLogFileName + "_" + str(i) + ".log", "r"),  False)
        ThroughputList2.append(t)
        LatencyList2.append(l)
        packetLossList2.append(p)
        RssiList2.append(r)
        SnrList2.append(s)

    ThroughputList2 = pd.DataFrame(ThroughputList2)
    ThroughputList2 = ThroughputList2.T
    
    
    LatencyList2 = pd.DataFrame(LatencyList2)
    LatencyList2 = LatencyList2.T
    

    packetLossList2 = pd.DataFrame(packetLossList2)
    packetLossList2 = packetLossList2.T
    

    RssiList2 = pd.DataFrame(RssiList2)
    RssiList2 = RssiList2.T
    

    SnrList2 = pd.DataFrame(SnrList2)
    SnrList2 = SnrList2.T

    # 3
    ThroughputList3 = []
    LatencyList3 = []
    packetLossList3 = []
    RssiList3 = []
    SnrList3 = []
    for i in range(expNumber + 1):
        t, l, p, r, s = cal_metric(open(logFolderName3 + senderLogFileName + "_" + str(
            i) + ".log", "r"), open(logFolderName3 + receiverLogFileName + "_" + str(i) + ".log", "r"),  False)
        ThroughputList3.append(t)
        LatencyList3.append(l)
        packetLossList3.append(p)
        RssiList3.append(r)
        SnrList3.append(s)

    ThroughputList3 = pd.DataFrame(ThroughputList3)
    ThroughputList3 = ThroughputList3.T

    LatencyList3 = pd.DataFrame(LatencyList3)
    LatencyList3 = LatencyList3.T
    

    packetLossList3 = pd.DataFrame(packetLossList3)
    packetLossList3 = packetLossList3.T
    

    RssiList3 = pd.DataFrame(RssiList3)
    RssiList3 = RssiList3.T
    

    SnrList3 = pd.DataFrame(SnrList3)
    SnrList3 = SnrList3.T
    
    
    
    # Draw Fig
    colors = ["blue", "red", "green", 'purple', 'brown']
    # labels = ["20", "30", "40"]
    x = [0,20,30, 40]
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    # Throughput
    ThroughputList = []
    ThroughputList.append(ThroughputList1[0])
    ThroughputList.append(ThroughputList2[0])
    ThroughputList.append(ThroughputList3[0])
    
    labels = ["20", "30", "40"]

    for i in range(3):
        plt.plot(data=ThroughputList[i],  errorbar=('ci', 95))
    plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    plt.ylabel("Throughput (kbps)", fontsize=my_fontsize)
    plt.xticks(x,  fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.legend(labels, loc="upper center", fancybox=False, labelspacing=0.05, handletextpad=0.5, ncol=4, borderpad=0.25,
               title="", framealpha=1, columnspacing=0.2, fontsize=my_fontsize, bbox_to_anchor=(0.5, 1.19))
    plt.savefig(figFolder + compare +  "throughput_depth_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + compare + "throughput_depth_lora.eps", dpi=300, bbox_inches="tight")
    plt.clf()
    
    # # Latency
    # LatencyList = pd.DataFrame({"20": LatencyList1[0]})
    # LatencyList["30"] = LatencyList2[0]
    # LatencyList["40"] = LatencyList3[0]



    # sns.barplot(data=LatencyList,  errorbar=('ci', 95),
    #             errwidth=10, width=width)
    # plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    # plt.ylabel("Latnecy (ms)", fontsize=my_fontsize)
    # plt.xticks(x, labels, fontsize=my_fontsize)
    # plt.yticks(fontsize=my_fontsize)
    # plt.savefig(figFolder + compare + "latency_depth_lora.svg", dpi=300, bbox_inches="tight")
    # plt.savefig(figFolder + compare + "latency_depth_lora.eps", dpi=300, bbox_inches="tight")
    # plt.clf()
    
    # # Packet loss rate
    # packetLossList = pd.DataFrame({"20": packetLossList1[0]})
    # packetLossList["30"] = packetLossList2[0]
    # packetLossList["40"] = packetLossList3[0]

    # sns.barplot(data=packetLossList,  errorbar=('ci', 95),
    #             errwidth=10, width=width)
    # plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    # plt.ylabel("Packet Loss Rate (%)", fontsize=my_fontsize)
    # plt.xticks(x, labels, fontsize=my_fontsize)
    # plt.yticks(fontsize=my_fontsize)
    # plt.savefig(figFolder + compare + "packetlossrate_depth_lora.svg",
    #             dpi=300, bbox_inches="tight")
    # plt.savefig(figFolder + compare + "packetlossrate_depth_lora.eps",
    #             dpi=300, bbox_inches="tight")
    # plt.clf()
    
    # # RSSI
    # RssiList = pd.DataFrame({"20": RssiList1[0]})
    # RssiList["30"] = RssiList2[0]
    # RssiList["40"] = RssiList3[0]


    # sns.barplot(data=RssiList,  errorbar=('ci', 95),
    #             errwidth=10, width=width)
    # plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    # plt.ylabel("RSSI (dBm)", fontsize=my_fontsize)
    # plt.xticks(x, labels, fontsize=my_fontsize)
    # plt.yticks(fontsize=my_fontsize)
    # plt.savefig(figFolder + compare + "rssi_depth_lora.svg",
    #             dpi=300, bbox_inches="tight")
    # plt.savefig(figFolder + compare + "rssi_depth_lora.eps",
    #             dpi=300, bbox_inches="tight")
    # plt.clf()
    
    # # SNR
    # SnrList = pd.DataFrame({"20": SnrList1[0]})
    # SnrList["30"] = SnrList2[0]
    # SnrList["40"] = SnrList3[0]

    # sns.barplot(data=SnrList,  errorbar=('ci', 95),
    #             errwidth=10, width=width)
    # plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    # plt.ylabel("SNR (dB)", fontsize=my_fontsize)
    # plt.xticks(x, labels, fontsize=my_fontsize)
    # plt.yticks(fontsize=my_fontsize)
    # plt.savefig(figFolder + compare + "snr_depth_lora.svg",
    #             dpi=300, bbox_inches="tight")
    # plt.savefig(figFolder + compare + "snr_depth_lora.eps",
    #             dpi=300, bbox_inches="tight")
    # plt.clf()

if __name__ == "__main__":
    
    # Args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--expNumber", type=int, default=0)
    args = parser.parse_args()
    
    draw_compare_line(args.expNumber)