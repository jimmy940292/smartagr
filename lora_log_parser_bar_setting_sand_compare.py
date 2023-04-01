from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd
import matplotlib.ticker as ticker

logFolderName1 = "fishtank_20cm_300cc_sand_M31_7pm/D4B500T15_"
logFolderName2 = "fishtank_20cm_600cc_sand_M31_7pm/D4B500T15_"
logFolderName3 = "fishtank_20cm_1200cc_sand_M31_7pm/D4B500T15_"
logFolderName4 = "fishtank_20cm_2400cc_sand_M31_7pm/D4B500T15_"
senderLogFileName = "lora_send"
receiverLogFileName = "lora_recv"
figFolder = "fig/lora/"
compare = "sand_"

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
        
    ThroughputList1 = pd.DataFrame(ThroughputList1)
    ThroughputList1 = ThroughputList1.T
    ThroughputList1['Avg'] = (ThroughputList1[0] + ThroughputList1[1] + ThroughputList1[2])/ 3 
  
    LatencyList1 = pd.DataFrame(LatencyList1)
    LatencyList1 = LatencyList1.T
    LatencyList1['Avg'] = (LatencyList1[0] + LatencyList1[1] + LatencyList1[2] ) /3
    
    packetLossList1 = pd.DataFrame(packetLossList1)
    packetLossList1 = packetLossList1.T
    packetLossList1['Avg'] = (packetLossList1[0] + packetLossList1[1] + packetLossList1[2] ) /3
  
    RssiList1 = pd.DataFrame(RssiList1)
    RssiList1 = RssiList1.T
    RssiList1['Avg'] = (RssiList1[0] + RssiList1[1] + RssiList1[2] ) / 3
    
    SnrList1 = pd.DataFrame(SnrList1)
    SnrList1 = SnrList1.T
    SnrList1['Avg'] = (SnrList1[0] + SnrList1[1] + SnrList1[2]) / 3
    
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
    ThroughputList2['Avg'] = (ThroughputList2[0] + ThroughputList2[1] + ThroughputList2[2] ) / 3
    
    LatencyList2 = pd.DataFrame(LatencyList2)
    LatencyList2 = LatencyList2.T
    LatencyList2['Avg'] = (LatencyList2[0] + LatencyList2[1] + LatencyList2[2] ) /3

    packetLossList2 = pd.DataFrame(packetLossList2)
    packetLossList2 = packetLossList2.T
    packetLossList2['Avg'] = (packetLossList2[0] + packetLossList2[1] + packetLossList2[2] ) /3

    RssiList2 = pd.DataFrame(RssiList2)
    RssiList2 = RssiList2.T
    RssiList2['Avg'] = (RssiList2[0] + RssiList2[1] + RssiList2[2] ) / 3

    SnrList2 = pd.DataFrame(SnrList2)
    SnrList2 = SnrList2.T
    SnrList2['Avg'] = (SnrList2[0] + SnrList2[1] + SnrList2[2]) / 3

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
    ThroughputList3['Avg'] = (ThroughputList3[0] + ThroughputList3[1] + ThroughputList3[2]) /3
    LatencyList3 = pd.DataFrame(LatencyList3)
    LatencyList3 = LatencyList3.T
    LatencyList3['Avg'] = (LatencyList3[0] + LatencyList3[1] + LatencyList3[2] ) / 3

    packetLossList3 = pd.DataFrame(packetLossList3)
    packetLossList3 = packetLossList3.T
    packetLossList3['Avg'] = (packetLossList3[0] + packetLossList3[1] + packetLossList3[2] ) / 3

    RssiList3 = pd.DataFrame(RssiList3)
    RssiList3 = RssiList3.T
    RssiList3['Avg'] = (RssiList3[0] + RssiList3[1] + RssiList3[2] ) /3

    SnrList3 = pd.DataFrame(SnrList3)
    SnrList3 = SnrList3.T
    SnrList3['Avg'] = (SnrList3[0] + SnrList3[1] + SnrList3[2] ) /3
    
    # 4
    ThroughputList4 = []
    LatencyList4 = []
    packetLossList4 = []
    RssiList4 = []
    SnrList4 = []
    for i in range(expNumber + 1):
        t, l, p, r, s = cal_metric(open(logFolderName4 + senderLogFileName + "_" + str(
            i) + ".log", "r"), open(logFolderName4 + receiverLogFileName + "_" + str(i) + ".log", "r"),  False)
        ThroughputList4.append(t)
        LatencyList4.append(l)
        packetLossList4.append(p)
        RssiList4.append(r)
        SnrList4.append(s)

    ThroughputList4 = pd.DataFrame(ThroughputList4)
    ThroughputList4 = ThroughputList4.T
    ThroughputList4['Avg'] = (
        ThroughputList4[0] + ThroughputList4[1] + ThroughputList4[2]) / 3
    LatencyList4 = pd.DataFrame(LatencyList4)
    LatencyList4 = LatencyList4.T
    LatencyList4['Avg'] = (
        LatencyList4[0] + LatencyList4[1] + LatencyList4[2]) / 3

    packetLossList4 = pd.DataFrame(packetLossList4)
    packetLossList4 = packetLossList4.T
    packetLossList4['Avg'] = (
        packetLossList4[0] + packetLossList4[1] + packetLossList4[2]) / 3

    RssiList4 = pd.DataFrame(RssiList4)
    RssiList4 = RssiList4.T
    RssiList4['Avg'] = (RssiList4[0] + RssiList4[1] + RssiList4[2]) / 3

    SnrList4 = pd.DataFrame(SnrList4)
    SnrList4 = SnrList4.T
    SnrList4['Avg'] = (SnrList4[0] + SnrList4[1] + SnrList4[2]) / 3
    
    # Draw Fig
    colors = ["blue", "red", "green", 'purple', 'brown']
    labels = ["300", "600", "1200", "2400"]
    x = [0,1,2, 3]
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    # Throughput
    ThroughputList = pd.DataFrame({"300cc":ThroughputList1["Avg"]})
    ThroughputList["600cc"] = ThroughputList2["Avg"]
    ThroughputList["1200cc"] = ThroughputList3["Avg"]
    ThroughputList["2400cc"] = ThroughputList3["Avg"]
        
    sns.barplot(data=ThroughputList,  errorbar=('ci', 95), errwidth=10, width=width)
    plt.xlabel("Water (cc)", fontsize=my_fontsize)
    plt.ylabel("Throughput (kbps)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + compare +  "throughput_moisture_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + compare + "throughput_moisture_lora.eps", dpi=300, bbox_inches="tight")
    plt.clf()
    
    # Latency
    LatencyList = pd.DataFrame({"300cc": LatencyList1["Avg"]})
    LatencyList["600cc"] = LatencyList2["Avg"]
    LatencyList["1200cc"] = LatencyList3["Avg"]
    LatencyList["2400cc"] = LatencyList4["Avg"]


    sns.barplot(data=LatencyList,  errorbar=('ci', 95),
                errwidth=10, width=width)
    plt.xlabel("Water (cc)", fontsize=my_fontsize)
    plt.ylabel("Latnecy (ms)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + compare + "latency_moisture_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + compare + "latency_moisture_lora.eps", dpi=300, bbox_inches="tight")
    plt.clf()
    
    # Packet loss rate
    packetLossList = pd.DataFrame({"300cc": packetLossList1["Avg"]})
    packetLossList["600cc"] = packetLossList2["Avg"]
    packetLossList["1200cc"] = packetLossList3["Avg"]
    packetLossList["2400cc"] = packetLossList4["Avg"]

    sns.barplot(data=packetLossList,  errorbar=('ci', 95),
                errwidth=10, width=width)
    plt.xlabel("Water (cc)", fontsize=my_fontsize)
    plt.ylabel("Packet Loss Rate (%)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + compare + "packetlossrate_moisture_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + compare + "packetlossrate_moisture_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()
    
    # RSSI
    RssiList = pd.DataFrame({"300cc": RssiList1["Avg"]})
    RssiList["600cc"] = RssiList2["Avg"]
    RssiList["1200cc"] = RssiList3["Avg"]
    RssiList["2400cc"] = RssiList4["Avg"]


    sns.barplot(data=RssiList,  errorbar=('ci', 95),
                errwidth=10, width=width)
    plt.xlabel("Water (cc)", fontsize=my_fontsize)
    plt.ylabel("RSSI (dBm)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + compare + "rssi_moisture_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + compare + "rssi_moisture_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()
    
    # SNR
    SnrList = pd.DataFrame({"300cc": SnrList1["Avg"]})
    SnrList["600cc"] = SnrList2["Avg"]
    SnrList["1200cc"] = SnrList3["Avg"]
    SnrList["2400cc"] = SnrList4["Avg"]

    sns.barplot(data=SnrList,  errorbar=('ci', 95),
                errwidth=10, width=width)
    plt.xlabel("Water (cc)", fontsize=my_fontsize)
    plt.ylabel("SNR (dB)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + compare + "snr_moisture_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + compare + "snr_moisture_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

if __name__ == "__main__":
    
    # Args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--expNumber", type=int, default=0)
    args = parser.parse_args()
    
    draw_compare_line(args.expNumber)