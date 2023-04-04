from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd
import matplotlib.ticker as ticker

# logFolderName1 = "results/D10_B20_S1_M29/"
# logFolderName2 = "results/D20_B20_S1_M29/"
# logFolderName3 = "results/D40_B20_S1_M29/"
# logFolderName4 = "results/D80_B20_S1_M29/"
# logFolderName5 = "results/D160_B20_S1_M29/"

# logFolderNames = ["fishtank_20cm_dry_sand_M31_6pm/D4B500T15_", "fishtank_20cm_300cc_sand_M31_7pm/D4B500T15_", 
    # "fishtank_20cm_600cc_sand_M31_7pm/D4B500T15_", "fishtank_20cm_1200cc_sand_M31_7pm/D4B500T15_", 
    # "fishtank_20cm_2400cc_sand_M31_7pm/D4B500T15_"]

# logFolderNames = ["results/D10_B20_S1_M29/", "results/D20_B20_S1_M29/", 
#     "results/D40_B20_S1_M29/", "results/D80_B20_S1_M29/", 
#     "results/D160_B20_S1_M29/"]

logFolderNames = ["rock/rock_20/D4B500T15_", "rock/rock_30/D4B500T15_", 
    "rock/rock_40/D4B500T15_"]

senderLogFileName = "lora_send"
receiverLogFileName = "lora_recv"

distances = ["10/", "20/", "30/"]

# figFolder = "fig/moisture_compare/lora/"
# figFolder = "fig/distance_compare/lora/"
figFolder = "fig/depth_compare/lora/"

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
                receivePacket[recvIndex].packetSize * 8.0 / 1000.0 )  # kbps
            latencyList.append(delta)  # ms
            rssiList.append(receivePacket[recvIndex].rssi)
            snrList.append(receivePacket[recvIndex].snr)
            recvIndex += 1

    senderLogFile.close()
    receiverLogFile.close()

    return sum(throughputList) / 10.0, latencyList, lostPacket , rssiList, snrList


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
    ThroughputList1['Avg'] = (ThroughputList1[0] + ThroughputList1[1] + ThroughputList1[2] + ThroughputList1[3] + ThroughputList1[4] + ThroughputList1[5] +
                              ThroughputList1[6] + ThroughputList1[7] + ThroughputList1[8] + ThroughputList1[9] + ThroughputList1[10] + ThroughputList1[11]) / 12
  
    LatencyList1 = pd.DataFrame(LatencyList1)
    LatencyList1 = LatencyList1.T
    LatencyList1['Avg'] = (LatencyList1[0] + LatencyList1[1] + LatencyList1[2] + LatencyList1[3] + LatencyList1[4] + LatencyList1[5] +
                           LatencyList1[6] + LatencyList1[7] + LatencyList1[8] + LatencyList1[9] + LatencyList1[10] + LatencyList1[11]) / 12
    
    packetLossList1 = pd.DataFrame(packetLossList1)
    packetLossList1 = packetLossList1.T
    packetLossList1['Avg'] = (packetLossList1[0] + packetLossList1[1] + packetLossList1[2] + packetLossList1[3] + packetLossList1[4] + packetLossList1[5] +
                              packetLossList1[6] + packetLossList1[7] + packetLossList1[8] + packetLossList1[9] + packetLossList1[10] + packetLossList1[11]) / 12
  
    RssiList1 = pd.DataFrame(RssiList1)
    RssiList1 = RssiList1.T
    RssiList1['Avg'] = (RssiList1[0] + RssiList1[1] + RssiList1[2] + RssiList1[3] + RssiList1[4] + RssiList1[5] +
                        RssiList1[6] + RssiList1[7] + RssiList1[8] + RssiList1[9] + RssiList1[10] + RssiList1[11]) / 12
    
    SnrList1 = pd.DataFrame(SnrList1)
    SnrList1 = SnrList1.T
    SnrList1['Avg'] = (SnrList1[0] + SnrList1[1] + SnrList1[2] + SnrList1[3] + SnrList1[4] + SnrList1[5] +
                       SnrList1[6] + SnrList1[7] + SnrList1[8] + SnrList1[9] + SnrList1[10] + SnrList1[11]) / 12
    
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
    ThroughputList2['Avg'] = (ThroughputList2[0] + ThroughputList2[1] + ThroughputList2[2] + ThroughputList2[3] + ThroughputList2[4] + ThroughputList2[5] +
                              ThroughputList2[6] + ThroughputList2[7] + ThroughputList2[8] + ThroughputList2[9] + ThroughputList2[10] + ThroughputList2[11]) / 12
    
    LatencyList2 = pd.DataFrame(LatencyList2)
    LatencyList2 = LatencyList2.T
    LatencyList2['Avg'] = (LatencyList2[0] + LatencyList2[1] + LatencyList2[2] + LatencyList2[3] + LatencyList2[4] + LatencyList2[5] +
                           LatencyList2[6] + LatencyList2[7] + LatencyList2[8] + LatencyList2[9] + LatencyList2[10] + LatencyList2[11]) / 12

    packetLossList2 = pd.DataFrame(packetLossList2)
    packetLossList2 = packetLossList2.T
    packetLossList2['Avg'] = (packetLossList2[0] + packetLossList2[1] + packetLossList2[2] + packetLossList2[3] + packetLossList2[4] + packetLossList2[5] +
                              packetLossList2[6] + packetLossList2[7] + packetLossList2[8] + packetLossList2[9] + packetLossList2[10] + packetLossList2[11]) / 12

    RssiList2 = pd.DataFrame(RssiList2)
    RssiList2 = RssiList2.T
    RssiList2['Avg'] = (RssiList2[0] + RssiList2[1] + RssiList2[2] + RssiList2[3] + RssiList2[4] + RssiList2[5] +
                        RssiList2[6] + RssiList2[7] + RssiList2[8] + RssiList2[9] + RssiList2[10] + RssiList2[11]) / 12

    SnrList2 = pd.DataFrame(SnrList2)
    SnrList2 = SnrList2.T
    SnrList2['Avg'] = (SnrList2[0] + SnrList2[1] + SnrList2[2] + SnrList2[3] + SnrList2[4] + SnrList2[5] +
                       SnrList2[6] + SnrList2[7] + SnrList2[8] + SnrList2[9] + SnrList2[10] + SnrList2[11]) / 12

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
    ThroughputList3['Avg'] = (ThroughputList3[0] + ThroughputList3[1] + ThroughputList3[2] + ThroughputList3[3] + ThroughputList3[4] + ThroughputList3[5] +
                              ThroughputList3[6] + ThroughputList3[7] + ThroughputList3[8] + ThroughputList3[9] + ThroughputList3[10] + ThroughputList3[11]) / 12
    
    LatencyList3 = pd.DataFrame(LatencyList3)
    LatencyList3 = LatencyList3.T
    LatencyList3['Avg'] = (LatencyList3[0] + LatencyList3[1] + LatencyList3[2] + LatencyList3[3] + LatencyList3[4] + LatencyList3[5] +
                           LatencyList3[6] + LatencyList3[7] + LatencyList3[8] + LatencyList3[9] + LatencyList3[10] + LatencyList3[11]) / 12

    packetLossList3 = pd.DataFrame(packetLossList3)
    packetLossList3 = packetLossList3.T
    packetLossList3['Avg'] = (packetLossList3[0] + packetLossList3[1] + packetLossList3[2] + packetLossList3[3] + packetLossList3[4] + packetLossList3[5] +
                              packetLossList3[6] + packetLossList3[7] + packetLossList3[8] + packetLossList3[9] + packetLossList3[10] + packetLossList3[11]) / 12

    RssiList3 = pd.DataFrame(RssiList3)
    RssiList3 = RssiList3.T
    RssiList3['Avg'] = (RssiList3[0] + RssiList3[1] + RssiList3[2] + RssiList3[3] + RssiList3[4] + RssiList3[5] +
                        RssiList3[6] + RssiList3[7] + RssiList3[8] + RssiList3[9] + RssiList3[10] + RssiList3[11]) / 12

    SnrList3 = pd.DataFrame(SnrList3)
    SnrList3 = SnrList3.T
    SnrList3['Avg'] = (SnrList3[0] + SnrList3[1] + SnrList3[2] + SnrList3[3] + SnrList3[4] + SnrList3[5] +
                       SnrList3[6] + SnrList3[7] + SnrList3[8] + SnrList3[9] + SnrList3[10] + SnrList3[11]) / 12
    
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
    ThroughputList4['Avg'] = (ThroughputList4[0] + ThroughputList4[1] + ThroughputList4[2] + ThroughputList4[3] + ThroughputList4[4] + ThroughputList4[5] +
                              ThroughputList4[6] + ThroughputList4[7] + ThroughputList4[8] + ThroughputList4[9] + ThroughputList4[10] + ThroughputList4[11]) / 12
    
    LatencyList4 = pd.DataFrame(LatencyList4)
    LatencyList4 = LatencyList4.T
    LatencyList4['Avg'] = (LatencyList4[0] + LatencyList4[1] + LatencyList4[2] + LatencyList4[3] + LatencyList4[4] + LatencyList4[5] +
                           LatencyList4[6] + LatencyList4[7] + LatencyList4[8] + LatencyList4[9] + LatencyList4[10] + LatencyList4[11]) / 12

    packetLossList4 = pd.DataFrame(packetLossList4)
    packetLossList4 = packetLossList4.T
    packetLossList4['Avg'] = (packetLossList4[0] + packetLossList4[1] + packetLossList4[2] + packetLossList4[3] + packetLossList4[4] + packetLossList4[5] +
                              packetLossList4[6] + packetLossList4[7] + packetLossList4[8] + packetLossList4[9] + packetLossList4[10] + packetLossList4[11]) / 12

    RssiList4 = pd.DataFrame(RssiList4)
    RssiList4 = RssiList4.T
    RssiList4['Avg'] = (RssiList4[0] + RssiList4[1] + RssiList4[2] + RssiList4[3] + RssiList4[4] + RssiList4[5] +
                        RssiList4[6] + RssiList4[7] + RssiList4[8] + RssiList4[9] + RssiList4[10] + RssiList4[11]) / 12

    SnrList4 = pd.DataFrame(SnrList4)
    SnrList4 = SnrList4.T
    SnrList4['Avg'] = (SnrList4[0] + SnrList4[1] + SnrList4[2] + SnrList4[3] + SnrList4[4] + SnrList4[5] +
                       SnrList4[6] + SnrList4[7] + SnrList4[8] + SnrList4[9] + SnrList4[10] + SnrList4[11]) / 12
    
    # 5
    ThroughputList5 = []
    LatencyList5 = []
    packetLossList5 = []
    RssiList5 = []
    SnrList5 = []
    for i in range(expNumber + 1):
        t, l, p, r, s = cal_metric(open(logFolderName5 + senderLogFileName + "_" + str(
            i) + ".log", "r"), open(logFolderName5 + receiverLogFileName + "_" + str(i) + ".log", "r"),  False)
        ThroughputList5.append(t)
        LatencyList5.append(l)
        packetLossList5.append(p)
        RssiList5.append(r)
        SnrList5.append(s)

    ThroughputList5 = pd.DataFrame(ThroughputList5)
    ThroughputList5 = ThroughputList5.T
    ThroughputList5['Avg'] = (ThroughputList5[0] + ThroughputList5[1] + ThroughputList5[2] + ThroughputList5[3] + ThroughputList5[4] + ThroughputList5[5] +
                              ThroughputList5[6] + ThroughputList5[7] + ThroughputList5[8] + ThroughputList5[9] + ThroughputList5[10] + ThroughputList5[11]) / 12
    
    LatencyList5 = pd.DataFrame(LatencyList5)
    LatencyList5 = LatencyList5.T
    LatencyList5['Avg'] = (LatencyList5[0] + LatencyList5[1] + LatencyList5[2] + LatencyList5[3] + LatencyList5[4] + LatencyList5[5] +
                           LatencyList5[6] + LatencyList5[7] + LatencyList5[8] + LatencyList5[9] + LatencyList5[10] + LatencyList5[11]) / 12

    packetLossList5 = pd.DataFrame(packetLossList5)
    packetLossList5 = packetLossList5.T
    packetLossList5['Avg'] = (packetLossList5[0] + packetLossList5[1] + packetLossList5[2] + packetLossList5[3] + packetLossList5[4] + packetLossList5[5] +
                              packetLossList5[6] + packetLossList5[7] + packetLossList5[8] + packetLossList5[9] + packetLossList5[10] + packetLossList5[11]) / 12

    RssiList5 = pd.DataFrame(RssiList5)
    RssiList5 = RssiList5.T
    RssiList5['Avg'] = (RssiList5[0] + RssiList5[1] + RssiList5[2] + RssiList5[3] + RssiList5[4] + RssiList5[5] +
                        RssiList4[6] + RssiList5[7] + RssiList5[8] + RssiList5[9] + RssiList5[10] + RssiList5[11]) / 12

    SnrList5 = pd.DataFrame(SnrList5)
    SnrList5 = SnrList5.T
    SnrList5['Avg'] = (SnrList5[0] + SnrList5[1] + SnrList5[2] + SnrList5[3] + SnrList5[4] + SnrList5[5] +
                       SnrList5[6] + SnrList5[7] + SnrList5[8] + SnrList5[9] + SnrList5[10] + SnrList5[11]) / 12

    # Draw Fig
    colors = ["blue", "red", "green", 'purple', 'brown']
    labels = ["10", "20", "40", "80", "160"]
    x = [0,1,2,3,4]
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    # Throughput
    ThroughputList = pd.DataFrame({"10cm":ThroughputList1["Avg"]})
    ThroughputList["20cm"] = ThroughputList2["Avg"]
    ThroughputList["40cm"] = ThroughputList3["Avg"]
    ThroughputList["80cm"] = ThroughputList4["Avg"]
    ThroughputList["160cm"] = ThroughputList5["Avg"]
        
    sns.barplot(data=ThroughputList,  errorbar=(
        'ci', 95), errwidth=10, width=width)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("Throughput (kbps)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(plt.yticks()[0], [f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    plt.tight_layout()
    plt.savefig(figFolder + "throughput_distance_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "throughput_distance_lora.eps", dpi=300, bbox_inches="tight")
    plt.clf()
    
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    
    # Latency
    LatencyList = pd.DataFrame({"10cm": LatencyList1["Avg"]})
    LatencyList["20cm"] = LatencyList2["Avg"]
    LatencyList["40cm"] = LatencyList3["Avg"]
    LatencyList["80cm"] = LatencyList4["Avg"]
    LatencyList["160cm"] = LatencyList5["Avg"]

    sns.barplot(data=LatencyList,  errorbar=('ci', 95),
                errwidth=10, width=width)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("Latnecy (ms)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(plt.yticks()[0], [f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    plt.tight_layout()
    plt.savefig(figFolder + "latency_distance_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "latency_distance_lora.eps", dpi=300, bbox_inches="tight")
    plt.clf()
    
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    
    # Packet loss rate
    packetLossList = pd.DataFrame({"10cm": packetLossList1["Avg"]})
    packetLossList["20cm"] = packetLossList2["Avg"]
    packetLossList["40cm"] = packetLossList3["Avg"]
    packetLossList["80cm"] = packetLossList4["Avg"]
    packetLossList["160cm"] = packetLossList5["Avg"]

    sns.barplot(data=packetLossList,  errorbar=('ci', 95),
             errwidth=10, width=width)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("Packet loss rate (%)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(plt.yticks()[0], [f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    plt.tight_layout()
    plt.savefig(figFolder + "packetlossrate_distance_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "packetlossrate_distance_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()
    
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    
    # RSSI
    RssiList = pd.DataFrame({"10cm": RssiList1["Avg"]})
    RssiList["20cm"] = RssiList2["Avg"]
    RssiList["40cm"] = RssiList3["Avg"]
    RssiList["80cm"] = RssiList4["Avg"]
    RssiList["160cm"] = RssiList5["Avg"]

    sns.barplot(data=RssiList,  errorbar=('ci', 95),
                errwidth=10, width=width)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("RSSI (dBm)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(plt.yticks()[0], [f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    plt.tight_layout()
    plt.savefig(figFolder + "rssi_distance_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "rssi_distance_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()
    
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42
    
    # SNR
    SnrList = pd.DataFrame({"10cm": SnrList1["Avg"]})
    SnrList["20cm"] = SnrList2["Avg"]
    SnrList["40cm"] = SnrList3["Avg"]
    SnrList["80cm"] = SnrList4["Avg"]
    SnrList["160cm"] = SnrList5["Avg"]

    sns.barplot(data=SnrList,  errorbar=('ci', 95),
                  errwidth=10, width=width)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("SNR (dB)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(plt.yticks()[0], [f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    plt.tight_layout()
    plt.savefig(figFolder + "snr_distance_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "snr_distance_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()


def draw_distance_line(expNumber):
    ThroughputList = []
    LatencyList = []
    PacketLossList = []
    RssiList = []
    SnrList = []
    avgThroughputList = []
    avgLatencyList = []
    avgPacketLossList = []
    avgRssiList = []
    avgSnrList = []
    for i in range(len(logFolderNames)):
        folderName = logFolderNames[i]
        avgt = 0
        avgl = 0
        avgp = 0
        avgr = 0
        avgs = 0
        t = []
        l = []
        p = []
        r = []
        s = []
        for j in range(expNumber+1) :
            _t, _l, _p, _r, _s = cal_metric(open(folderName + senderLogFileName + "_" + str(
            j) + ".log", "r"), open(folderName + receiverLogFileName + "_" + str(j) + ".log", "r"))
            avgt += _t
            avgl += sum(_l) / len(_l)
            avgp += _p
            avgr += sum(_r) / len(_r)
            avgs += sum(_s) / len(_s)
            t.append(_t)
            l.append(sum(_l) / len(_l))
            p.append(_p)
            r.append(sum(_r) / len(_r))
            s.append(sum(_s) / len(_s))
        avgt /= (expNumber+1)
        avgl /= (expNumber+1)
        avgp /= (expNumber+1)
        avgr /= (expNumber+1)
        avgs /= (expNumber+1)
        avgThroughputList.append(avgt)
        avgLatencyList.append(avgl)
        avgPacketLossList.append(avgp)
        avgRssiList.append(avgr)
        avgSnrList.append(avgs)
        ThroughputList.append(t)
        LatencyList.append(l)
        PacketLossList.append(p)
        RssiList.append(r)
        SnrList.append(s)

    colors = ["blue", "red", "green", 'purple', 'brown']
    labels = ["10", "20", "40", "80", "160"]
    x = [10, 20, 40, 80, 160]
    z=[4000]*len(avgThroughputList)
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    # Throughput
    ThroughputList_err = []
    for i in range(len(ThroughputList)):
        ThroughputList_err.append(
            1.96*np.std(ThroughputList[i]) / np.sqrt(len(ThroughputList[i])))
    # sem = np.std(ThroughputList) / np.sqrt(len(ThroughputList))
    # z_score = 1.96
    # ThroughputList_err = z_score * sem
    plt.errorbar(x, avgThroughputList, yerr=ThroughputList_err, linewidth=20)
    plt.scatter(x, avgThroughputList, s=z, marker="o")

    x_major_locator = ticker.MultipleLocator(40)
    y_major_locator = ticker.MultipleLocator(0.1)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    y_major_locator = ticker.MultipleLocator(0.1)
    axes.yaxis.set_major_locator(y_major_locator)
    # sns.pointplot(x = np.arange(0, 5), y = ThroughputList, errorbar=('ci', 95), scale=2, dodge=1, join=True)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("Throughput (kbps)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(plt.yticks()[0], [f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    plt.xlim(0, 200)
    plt.tight_layout()
    plt.savefig(figFolder + "throughput_distance_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "throughput_distance_lora.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    # Latency
    LatencyList_err = []
    for i in range(len(LatencyList)):
        LatencyList_err.append(
            1.96*np.std(LatencyList[i]) / np.sqrt(len(LatencyList[i])))
    # sem = np.std(LatencyList) / np.sqrt(len(LatencyList))
    # z_score = 1.96
    # LatencyList_err = z_score * sem
    # print(LatencyList)
    # print(LatencyList_err)
    # print(avgLatencyList)
    plt.errorbar(x, avgLatencyList, yerr=LatencyList_err,linewidth=20)
    plt.scatter(x, avgLatencyList, s=z, marker="o")
    x_major_locator = ticker.MultipleLocator(40)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("Latency (ms)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(plt.yticks()[0], [f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    plt.xlim(0, 200)
    plt.tight_layout()
    plt.savefig(figFolder + "latency_distance_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "latency_distance_lora.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    # PacketLoss
    PacketLossList_err = []
    for i in range(len(PacketLossList)):
        PacketLossList_err.append(
            1.96*np.std(PacketLossList[i]) / np.sqrt(len(PacketLossList[i])))
    # sem = np.std(PacketLossList) / np.sqrt(len(PacketLossList))
    # z_score = 1.96
    # PacketLossList_err = z_score * sem
    plt.errorbar(x, avgPacketLossList, yerr=PacketLossList_err,linewidth=20)
    plt.scatter(x, avgPacketLossList, s=z, marker="o")
    plt.ylim(bottom=0)
    x_major_locator = ticker.MultipleLocator(40)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    y_major_locator = ticker.MultipleLocator(0.5)
    axes.yaxis.set_major_locator(y_major_locator)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("Packet Loss Rate (%)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(plt.yticks()[0], [f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    plt.xlim(0, 200)
    plt.ylim(0)
    plt.tight_layout()
    plt.savefig(figFolder + "packetLoss_distance_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "packetLoss_distance_lora.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    # Rssi
    RssiList_err = []
    for i in range(len(RssiList)):
        RssiList_err.append(
            1.96*np.std(RssiList[i]) / np.sqrt(len(RssiList[i])))
    # sem = np.std(RssiList) / np.sqrt(len(RssiList))
    # z_score = 1.96
    # RssiList_err = z_score * sem
    plt.errorbar(x, avgRssiList,yerr=RssiList_err, linewidth=20)
    plt.scatter(x, avgRssiList,s = z, marker="o")
    x_major_locator = ticker.MultipleLocator(40)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("RSSI (dBm)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    # plt.yticks(plt.yticks()[0], [f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    plt.xlim(0, 200)
    plt.ylim(-105, -80)
    plt.tight_layout()
    plt.savefig(figFolder + "rssi_distance_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "rssi_distance_lora.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    SnrList_err = []
    for i in range(len(SnrList)):
        SnrList_err.append(
            1.96*np.std(SnrList[i]) / np.sqrt(len(SnrList[i])))
    # sem = np.std(SnrList) / np.sqrt(len(SnrList))
    # z_score = 1.96
    # SnrList_err = z_score * sem
    plt.errorbar(x, avgSnrList, yerr=SnrList_err, linewidth=20)
    plt.scatter(x, avgSnrList, s=z, marker="o")
    x_major_locator = ticker.MultipleLocator(40)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("SNR (dB)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    # plt.yticks(plt.yticks()[0], [f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    plt.xlim(0, 200)
    plt.ylim(50, 60)
    plt.tight_layout()
    plt.savefig(figFolder + "snr_distance_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "snr_distance_lora.eps", dpi=300, bbox_inches="tight")
    plt.clf()


def draw_moisture_line(expNumber):
    ThroughputList = []
    LatencyList = []
    PacketLossList = []
    RssiList = []
    SnrList = []
    avgThroughputList = []
    avgLatencyList = []
    avgPacketLossList = []
    avgRssiList = []
    avgSnrList = []
    for i in range(len(logFolderNames)):
        folderName = logFolderNames[i]
        avgt = 0
        avgl = 0
        avgp = 0
        avgr = 0
        avgs = 0
        t = []
        l = []
        p = []
        r = []
        s = []
        for j in range(expNumber+1):
            _t, _l, _p, _r, _s = cal_metric(open(folderName + senderLogFileName + "_" + str(
                j) + ".log", "r"), open(folderName + receiverLogFileName + "_" + str(j) + ".log", "r"))
            avgt += _t
            avgl += sum(_l) / len(_l)
            avgp += _p
            avgr += sum(_r) / len(_r)
            avgs += sum(_s) / len(_s)
            t.append(_t)
            l.append(sum(_l) / len(_l))
            p.append(_p)
            r.append(sum(_r) / len(_r))
            s.append(sum(_s) / len(_s))
        avgt /= (expNumber+1)
        avgl /= (expNumber+1)
        avgp /= (expNumber+1)
        avgr /= (expNumber+1)
        avgs /= (expNumber+1)
        avgThroughputList.append(avgt)
        avgLatencyList.append(avgl)
        avgPacketLossList.append(avgp)
        avgRssiList.append(avgr)
        avgSnrList.append(avgs)
        ThroughputList.append(t)
        LatencyList.append(l)
        PacketLossList.append(p)
        RssiList.append(r)
        SnrList.append(s)

    colors = ["blue", "red", "green", 'purple', 'brown']
    labels = ["0", "600", "1200", "1800", "2400"]
    x = [0, 300, 600, 1200, 2400]
    z= [4000] * len(avgThroughputList)
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    # Throughput
    ThroughputList_err = []
    for i in range(len(ThroughputList)):
        ThroughputList_err.append(
            1.96*np.std(ThroughputList[i]) / np.sqrt(len(ThroughputList[i])))
    # sem = np.std(ThroughputList) / np.sqrt(len(ThroughputList))
    # z_score = 1.96
    # ThroughputList_err = z_score * sem

    plt.errorbar(x, avgThroughputList, yerr = ThroughputList_err, linewidth=20)
    plt.scatter(x, avgThroughputList,s = z, marker="o")

    x_major_locator = ticker.MultipleLocator(600)    
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    y_major_locator = ticker.MultipleLocator(2)
    axes.yaxis.set_major_locator(y_major_locator)
    # sns.pointplot(x = np.arange(0, 5), y = ThroughputList, errorbar=('ci', 95), scale=2, dodge=1, join=True)
    plt.xlabel("Water (ml)", fontsize=my_fontsize)
    plt.ylabel("Throughput (kbps)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    # plt.yticks(plt.yticks()[0], [f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    plt.xlim(-100, 2600)
    plt.ylim(0, 8.0)
    plt.tight_layout()
    plt.savefig(figFolder + "throughput_moisture_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "throughput_moisture_lora.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    # Latency
    LatencyList_err = []
    for i in range(len(LatencyList)):
        LatencyList_err.append(
            1.96*np.std(LatencyList[i]) / np.sqrt(len(LatencyList[i])))
    # sem = np.std(LatencyList) / np.sqrt(len(LatencyList))
    # z_score = 1.96
    # LatencyList_err = z_score * sem
    plt.errorbar(x, avgLatencyList, yerr = LatencyList_err, linewidth=20)
    plt.scatter(x, avgLatencyList, s=z, marker="o")

    x_major_locator = ticker.MultipleLocator(600)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    # y_major_locator = ticker.MultipleLocator(0.1)
    # axes.yaxis.set_major_locator(y_major_locator)
    plt.xlabel("Water (ml)", fontsize=my_fontsize)
    plt.ylabel("Latency (ms)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    # plt.yticks(plt.yticks()[0], [f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    plt.xlim(-100, 2600)
    plt.ylim(0, 66)
    plt.tight_layout()
    plt.savefig(figFolder + "latency_moisture_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "latency_moisture_lora.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    # PacketLoss
    PacketLossList_err = []
    for i in range(len(PacketLossList)):
        PacketLossList_err.append(
            1.96*np.std(PacketLossList[i]) / np.sqrt(len(PacketLossList[i])))
    # sem = np.std(PacketLossList) / np.sqrt(len(PacketLossList))
    # z_score = 1.96
    # PacketLossList_err = z_score * sem
    plt.errorbar(x, avgPacketLossList, yerr = PacketLossList_err, linewidth=20)
    plt.scatter(x, avgPacketLossList, s=z, marker="o")
    plt.ylim(bottom=0)
    x_major_locator = ticker.MultipleLocator(600)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    plt.xlabel("Water (ml)", fontsize=my_fontsize)
    plt.ylabel("Packet Loss Rate (%)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(plt.yticks()[0], [f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    plt.xlim(-100, 2600)
    plt.tight_layout()
    plt.savefig(figFolder + "packetLoss_moisture_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "packetLoss_moisture_lora.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    # Rssi
    RssiList_err = []
    for i in range(len(RssiList)):
        RssiList_err.append(
            1.96*np.std(RssiList[i]) / np.sqrt(len(RssiList[i])))
    # sem = np.std(RssiList) / np.sqrt(len(RssiList))
    # z_score = 1.96
    # RssiList_err = z_score * sem
    plt.errorbar(x, avgRssiList, yerr = RssiList_err, linewidth=20)
    plt.scatter(x, avgRssiList, s=z, marker="o")
    x_major_locator = ticker.MultipleLocator(600)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    plt.xlabel("Water (ml)", fontsize=my_fontsize)
    plt.ylabel("RSSI (dBm)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(plt.yticks()[0], [f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    plt.xlim(-100, 2600)
    plt.tight_layout()
    plt.savefig(figFolder + "rssi_moisture_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "rssi_moisture_lora.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    SnrList_err = []
    for i in range(len(SnrList)):
        SnrList_err.append(
            1.96*np.std(SnrList[i]) / np.sqrt(len(SnrList[i])))
    # sem = np.std(SnrList) / np.sqrt(len(SnrList))
    # z_score = 1.96
    # SnrList_err = z_score * sem
    plt.errorbar(x, avgSnrList, yerr = SnrList_err, linewidth=20)
    plt.scatter(x, avgSnrList, s=z, marker="o")
    x_major_locator = ticker.MultipleLocator(600)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    y_major_locator = ticker.MultipleLocator(2)
    axes.yaxis.set_major_locator(y_major_locator)
    plt.xlabel("Water (ml)", fontsize=my_fontsize)
    plt.ylabel("SNR (dB)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    # plt.yticks(plt.yticks()[0], [f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    plt.xlim(-100, 2600)
    plt.ylim(50)
    plt.tight_layout()
    plt.savefig(figFolder + "snr_moisture_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "snr_moisture_lora.eps", dpi=300, bbox_inches="tight")
    plt.clf()


def draw_depth_line(expNumber):
    ThroughputList = []
    LatencyList = []
    PacketLossList = []
    RssiList = []
    SnrList = []
    avgThroughputList = []
    avgLatencyList = []
    avgPacketLossList = []
    avgRssiList = []
    avgSnrList = []
    for i in range(len(logFolderNames)):
        folderName = logFolderNames[i]
        avgt = 0
        avgl = 0
        avgp = 0
        avgr = 0
        avgs = 0
        t = []
        l = []
        p = []
        r = []
        s = []
        for j in range(expNumber+1):
            _t, _l, _p, _r, _s = cal_metric(open(folderName + senderLogFileName + "_" + str(
                j) + ".log", "r"), open(folderName + receiverLogFileName + "_" + str(j) + ".log", "r"))
            avgt += _t
            avgl += sum(_l) / len(_l)
            avgp += _p
            avgr += sum(_r) / len(_r)
            avgs += sum(_s) / len(_s)
            t.append(_t)
            l.append(sum(_l) / len(_l))
            p.append(_p)
            r.append(sum(_r) / len(_r))
            s.append(sum(_s) / len(_s))
        avgt /= (expNumber+1)
        avgl /= (expNumber+1)
        avgp /= (expNumber+1)
        avgr /= (expNumber+1)
        avgs /= (expNumber+1)
        avgThroughputList.append(avgt)
        avgLatencyList.append(avgl)
        avgPacketLossList.append(avgp)
        avgRssiList.append(avgr)
        avgSnrList.append(avgs)
        ThroughputList.append(t)
        LatencyList.append(l)
        PacketLossList.append(p)
        RssiList.append(r)
        SnrList.append(s)

    colors = ["blue", "red", "green", 'purple', 'brown']
    labels = ["20", "30","40"]
    x = [20, 30, 40]
    z= [4000]*len(avgThroughputList)
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    # Throughput
    ThroughputList_err = []
    for i in range(len(ThroughputList)):
        ThroughputList_err.append(
            1.96*np.std(ThroughputList[i]) / np.sqrt(len(ThroughputList[i])))
    # sem = np.std(ThroughputList) / np.sqrt(len(ThroughputList))
    # z_score = 1.96
    # ThroughputList_err = z_score * sem
    plt.errorbar(x, avgThroughputList,  linewidth=20)
    plt.scatter(x, avgThroughputList, s=z, marker="o")
    x_major_locator = ticker.MultipleLocator(10)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    y_major_locator = ticker.MultipleLocator(0.1)
    axes.yaxis.set_major_locator(y_major_locator)
    # sns.pointplot(x = np.arange(0, 5), y = ThroughputList, errorbar=('ci', 95), scale=2, dodge=1, join=True)
    plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    plt.ylabel("Throughput (kbps)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(plt.yticks()[0], [
               f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    # plt.xlim(-100, 2600)
    plt.xlim(0, 50)
    plt.tight_layout()
    plt.savefig(figFolder + "throughput_depth_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "throughput_depth_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # Latency
    LatencyList_err = []
    for i in range(len(LatencyList)):
        LatencyList_err.append(
            1.96*np.std(LatencyList[i]) / np.sqrt(len(LatencyList[i])))
    # sem = np.std(LatencyList) / np.sqrt(len(LatencyList))
    # z_score = 1.96
    # LatencyList_err = z_score * sem
    plt.errorbar(x, avgLatencyList, linewidth=20)
    plt.scatter(x, avgLatencyList, s=z, marker="o")
    x_major_locator = ticker.MultipleLocator(10)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    plt.ylabel("Latency (ms)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(plt.yticks()[0], [
               f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    # plt.xlim(-100, 2600)
    plt.tight_layout()
    plt.xlim(0, 50)
    plt.savefig(figFolder + "latency_depth_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "latency_depth_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # PacketLoss
    PacketLossList_err = []
    for i in range(len(PacketLossList)):
        PacketLossList_err.append(
            1.96*np.std(PacketLossList[i]) / np.sqrt(len(PacketLossList[i])))
    # sem = np.std(PacketLossList) / np.sqrt(len(PacketLossList))
    # z_score = 1.96
    # PacketLossList_err = z_score * sem
    plt.errorbar(x, avgPacketLossList,  linewidth=20)
    plt.scatter(x, avgPacketLossList, s=z, marker="o")
    plt.ylim(bottom=0)
    x_major_locator = ticker.MultipleLocator(10)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    y_major_locator = ticker.MultipleLocator(0.5)
    axes.yaxis.set_major_locator(y_major_locator)
    plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    plt.ylabel("Packet Loss Rate (%)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(plt.yticks()[0], [
               f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    # plt.xlim(-100, 2600)
    plt.xlim(0, 50)
    plt.ylim(0.0)
    plt.tight_layout()
    plt.savefig(figFolder + "packetLoss_depth_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "packetLoss_depth_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # Rssi
    RssiList_err = []
    for i in range(len(RssiList)):
        RssiList_err.append(
            1.96*np.std(RssiList[i]) / np.sqrt(len(RssiList[i])))
    # sem = np.std(RssiList) / np.sqrt(len(RssiList))
    # z_score = 1.96
    # RssiList_err = z_score * sem
    plt.errorbar(x, avgRssiList,  linewidth=20)
    plt.scatter(x, avgRssiList, s=z, marker="o")
    x_major_locator = ticker.MultipleLocator(10)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    plt.ylabel("RSSI (dBm)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(plt.yticks()[0], [
               f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    # plt.xlim(-100, 2600)
    plt.xlim(0, 50)
    plt.tight_layout()
    plt.savefig(figFolder + "rssi_depth_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "rssi_depth_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    SnrList_err = []
    for i in range(len(SnrList)):
        SnrList_err.append(
            1.96*np.std(SnrList[i]) / np.sqrt(len(SnrList[i])))
    # sem = np.std(SnrList) / np.sqrt(len(SnrList))
    # z_score = 1.96
    # SnrList_err = z_score * sem
    plt.errorbar(x, avgSnrList,  linewidth=20)
    plt.scatter(x, avgSnrList, s=z, marker="o")
    x_major_locator = ticker.MultipleLocator(10)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    y_major_locator = ticker.MultipleLocator(0.1)
    axes.yaxis.set_major_locator(y_major_locator)
    plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    plt.ylabel("SNR (dB)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(plt.yticks()[0], [
               f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    # plt.xlim(-100, 2600)
    plt.xlim(0, 50)
    plt.tight_layout()
    plt.savefig(figFolder + "snr_depth_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "snr_depth_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

if __name__ == "__main__":
    
    # Args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--expNumber", type=int, default=0)
    args = parser.parse_args()
    
    # draw_moisture_line(args.expNumber)
    # draw_distance_line(args.expNumber)
    draw_depth_line(args.expNumber)