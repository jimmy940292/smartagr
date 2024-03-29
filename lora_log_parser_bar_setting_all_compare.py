from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd
import matplotlib.ticker as ticker

logFolderName1 = "fishtank_20cm_dry_sand_M31_6pm/D4B500T15_"
logFolderName2 = "results/D20_B20_S1_M29/"
logFolderName3 = "rock/rock_20/D4B500T15_"
senderLogFileName = "lora_send"
receiverLogFileName = "lora_recv"
figFolder = "fig/all/lora/"
compare = "soil_type_"

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
    for i in range(6):
        t, l, p, r, s = cal_metric(open(logFolderName1 + senderLogFileName + "_" + str(
            i) + ".log", "r"), open(logFolderName1 + receiverLogFileName + "_" + str(i) + ".log", "r"))

        ThroughputList1.append(t)
        LatencyList1.append(sum(l)/len(l))
        packetLossList1.append(p/len(l)*100)
        RssiList1.append(sum(r)/len(r))
        SnrList1.append(sum(s)/len(s))
        
    # ThroughputList1 = pd.DataFrame(ThroughputList1)
    # ThroughputList1 = ThroughputList1.T
    

    # # ThroughputList1['Avg'] = (ThroughputList1[0] + ThroughputList1[1] + ThroughputList1[2])/ 3 
  
    # LatencyList1 = pd.DataFrame(LatencyList1)
    # LatencyList1 = LatencyList1.T
    # # LatencyList1['Avg'] = (LatencyList1[0] + LatencyList1[1] + LatencyList1[2] ) /3
    
    # packetLossList1 = pd.DataFrame(packetLossList1)
    # packetLossList1 = packetLossList1.T
    # # packetLossList1['Avg'] = (packetLossList1[0] + packetLossList1[1] + packetLossList1[2] ) /3
  
    # RssiList1 = pd.DataFrame(RssiList1)
    # RssiList1 = RssiList1.T
    # # RssiList1['Avg'] = (RssiList1[0] + RssiList1[1] + RssiList1[2] ) / 3
    
    # SnrList1 = pd.DataFrame(SnrList1)
    # SnrList1 = SnrList1.T
    # SnrList1['Avg'] = (SnrList1[0] + SnrList1[1] + SnrList1[2]) / 3
    
    # 2
    ThroughputList2 = []
    LatencyList2 = []
    packetLossList2 = []
    RssiList2 = []
    SnrList2 = []
    for i in range(12):
        t, l, p, r, s = cal_metric(open(logFolderName2 + senderLogFileName + "_" + str(
            i) + ".log", "r"), open(logFolderName2 + receiverLogFileName + "_" + str(i) + ".log", "r"),  False)
        ThroughputList2.append(t)
        LatencyList2.append(sum(l)/len(l))
        packetLossList2.append(p/len(l)*100)
        RssiList2.append(sum(r)/len(r))
        SnrList2.append(sum(s)/len(s))

    # ThroughputList2 = pd.DataFrame(ThroughputList2)
    # ThroughputList2 = ThroughputList2.T
    # # ThroughputList2['Avg'] = (ThroughputList2[0] + ThroughputList2[1] + ThroughputList2[2] ) / 3
    
    # LatencyList2 = pd.DataFrame(LatencyList2)
    # LatencyList2 = LatencyList2.T
    # # LatencyList2['Avg'] = (LatencyList2[0] + LatencyList2[1] + LatencyList2[2] ) /3

    # packetLossList2 = pd.DataFrame(packetLossList2)
    # packetLossList2 = packetLossList2.T
    # # packetLossList2['Avg'] = (packetLossList2[0] + packetLossList2[1] + packetLossList2[2] ) /3

    # RssiList2 = pd.DataFrame(RssiList2)
    # RssiList2 = RssiList2.T
    # # RssiList2['Avg'] = (RssiList2[0] + RssiList2[1] + RssiList2[2] ) / 3

    # SnrList2 = pd.DataFrame(SnrList2)
    # SnrList2 = SnrList2.T
    # SnrList2['Avg'] = (SnrList2[0] + SnrList2[1] + SnrList2[2]) / 3

    # 3
    ThroughputList3 = []
    LatencyList3 = []
    packetLossList3 = []
    RssiList3 = []
    SnrList3 = []
    for i in range(1):
        t, l, p, r, s = cal_metric(open(logFolderName3 + senderLogFileName + "_" + str(
            i) + ".log", "r"), open(logFolderName3 + receiverLogFileName + "_" + str(i) + ".log", "r"),  False)
        ThroughputList3.append(t)
        LatencyList3.append(sum(l)/len(l))
        packetLossList3.append(p/len(l)*100)
        RssiList3.append(sum(r)/len(r))
        SnrList3.append(sum(s)/len(s))

    # ThroughputList3 = pd.DataFrame(ThroughputList3)
    # ThroughputList3 = ThroughputList3.T
    # # ThroughputList3['Avg'] = (ThroughputList3[0] + ThroughputList3[1] + ThroughputList3[2]) /3
    # LatencyList3 = pd.DataFrame(LatencyList3)
    # LatencyList3 = LatencyList3.T
    # # LatencyList3['Avg'] = (LatencyList3[0] + LatencyList3[1] + LatencyList3[2] ) / 3

    # packetLossList3 = pd.DataFrame(packetLossList3)
    # packetLossList3 = packetLossList3.T
    # # packetLossList3['Avg'] = (packetLossList3[0] + packetLossList3[1] + packetLossList3[2] ) / 3

    # RssiList3 = pd.DataFrame(RssiList3)
    # RssiList3 = RssiList3.T
    # # RssiList3['Avg'] = (RssiList3[0] + RssiList3[1] + RssiList3[2] ) /3

    # SnrList3 = pd.DataFrame(SnrList3)
    # SnrList3 = SnrList3.T
    # SnrList3['Avg'] = (SnrList3[0] + SnrList3[1] + SnrList3[2] ) /3
    
    
    # Draw Fig
    colors = ["blue", "red", "green", 'purple', 'brown']
    labels = ["Sand", "Yellow", "Gravel"]
    x = [0,1,2]
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    # Throughput
    # ThroughputList = pd.DataFrame({"1":ThroughputList1[0]})
    # ThroughputList["2"] = ThroughputList2[0]
    # ThroughputList["3"] = ThroughputList3[0]
    
    ThroughputList = [[sum(ThroughputList1)/len(ThroughputList1)],
                      [sum(ThroughputList2)/len(ThroughputList2)],
                      [sum(ThroughputList3)/len(ThroughputList3)]]
   
        
    sns.barplot(data=ThroughputList,  errorbar=('ci', 95), errwidth=20, width=width, palette=colors)
    # plt.xlabel("Soil Type", fontsize=my_fontsize)
    plt.ylabel("Throughput (kbps)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.tight_layout()
    plt.savefig(figFolder + compare +  "throughput_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + compare + "throughput_lora.eps", dpi=300, bbox_inches="tight")
    plt.clf()
    
    # Latency
    # LatencyList = pd.DataFrame({"1": LatencyList1[0]})
    # LatencyList["2"] = LatencyList2[0]
    # LatencyList["3"] = LatencyList3[0]
    LatencyList = [[sum(LatencyList1)/len(LatencyList1)],
                   [sum(LatencyList2)/len(LatencyList2)],
                   [sum(LatencyList3)/len(LatencyList3)]]


    sns.barplot(data=LatencyList,  errorbar=('ci', 95),
                errwidth=20, width=width, palette=colors)
    # plt.xlabel("Soil Type", fontsize=my_fontsize)
    plt.ylabel("Latnecy (ms)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.tight_layout()
    plt.savefig(figFolder + compare + "latency_lora.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + compare + "latency_lora.eps", dpi=300, bbox_inches="tight")
    plt.clf()
    
    # Packet loss rate
    # packetLossList = pd.DataFrame({"1": packetLossList1[0]})
    # packetLossList["2"] = packetLossList2[0]
    # packetLossList["3"] = packetLossList3[0]

    packetLossList = [[sum(packetLossList1)/len(packetLossList1)],
                      [sum(packetLossList2)/len(packetLossList2)],
                      [sum(packetLossList3)/len(packetLossList3)]]


    sns.barplot(data=packetLossList,  errorbar=('ci', 95),
                errwidth=20, width=width, palette=colors)
    # plt.xlabel("Soil Type", fontsize=my_fontsize)
    plt.ylabel("Packet Loss Rate (%)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(plt.yticks()[0], [
        f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    plt.tight_layout()
    plt.savefig(figFolder + compare + "packetlossrate_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + compare + "packetlossrate_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()
    
    # RSSI
    # RssiList = pd.DataFrame({"1": RssiList1[0]})
    # RssiList["2"] = RssiList2[0]
    # RssiList["3"] = RssiList3[0]
    RssiList = [[sum(RssiList1)/len(RssiList1)],
                [sum(RssiList2)/len(RssiList2)],
                [sum(RssiList3)/len(RssiList3)]]


    sns.barplot(data=RssiList,  errorbar=('ci', 95),
                errwidth=20, width=width, palette=colors)
    # plt.xlabel("Soil Type", fontsize=my_fontsize)
    plt.ylabel("RSSI (dBm)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.tight_layout()
    plt.savefig(figFolder + compare + "rssi_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + compare + "rssi_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()
    
    
    
    # SNR
    # SnrList = pd.DataFrame({"1": SnrList1[0]})
    # SnrList["2"] = SnrList2[0]
    # SnrList["3"] = SnrList3[0]

    SnrList = [[sum(SnrList1)/len(SnrList1)],
               [sum(SnrList2)/len(SnrList2)],
               [sum(SnrList3)/len(SnrList3)]]

    sns.barplot(data=SnrList,  errorbar=('ci', 95),
                errwidth=20, width=width, palette=colors)
    # plt.xlabel("Soil Type", fontsize=my_fontsize)
    plt.ylabel("SNR (dB)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.tight_layout()
    plt.savefig(figFolder + compare + "snr_lora.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + compare + "snr_lora.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

if __name__ == "__main__":
    
    # Args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--expNumber", type=int, default=0)
    args = parser.parse_args()
    
    draw_compare_line(args.expNumber)