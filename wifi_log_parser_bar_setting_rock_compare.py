from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd
import matplotlib.ticker as ticker
import re

logFolderName1 = "rock/rock_20/T20_"
logFolderName2 = "rock/rock_30/T20_"
logFolderName3 = "rock/rock_40/T20_"

senderLogFileName = "wifi_send"
figFolder = "fig/rock/wifi/"
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


def parse_log_from_file(senderLogFile):

    # Throughput (Mb)
    pattern = "\[\s*\d\] \d+.\d+-\d+.\d+ sec\s*\d+.\d+ \wBytes\s*(\d+.\d+) Mbits\/sec\s*\d+.\d+ ms\s*\d+\/\s*\d+ \([\d]+|[\d+.\d+]%\)"
    throughput = 0.0
    for i, line in enumerate(open(senderLogFile, 'r')):
        if (re.match(pattern, line)):
            throughput = float(re.match(pattern, line).group(1))
            throughput *= 1000
            break

    # Throughput (Kb)
    pattern = "\[\s*\d\] \d+\.\d+\-\d+\.\d+ sec\s*\d+\.\d+ \wBytes\s*(\d+) Kbits\/sec\s*\d+.\d+ ms\s*\d+\/\s*\d+ \([\d]+|[\d+.\d+]%\)"
    for i, line in enumerate(open(senderLogFile, 'r')):
        if (re.match(pattern, line)):
            throughput = float(re.match(pattern, line).group(1))
            break

    # Latency
    pattern = "rtt min/avg/max/mdev = \d+.\d+/(\d+.\d+)/\d+.\d+/\d+.\d+ ms"
    latency = 0.0
    for i, line in enumerate(open(senderLogFile, 'r')):
        if (re.match(pattern, line)):
            latency = float(re.match(pattern, line).group(1))
            break

    # Packet loss rate (Mb)
    pattern = "\[\s*\d\] \d+.\d+-\d+.\d+ sec\s*\d+.\d+ \wBytes\s*\d+.\d+ Mbits\/sec\s*\d+.\d+ ms\s*\d+\/\s*\d+\s*\((\d+|\d+.\d+)%\)"
    packetlossrate = 0.0
    for i, line in enumerate(open(senderLogFile, 'r')):
        if (re.match(pattern, line)):
            packetlossrate = float(re.match(pattern, line).group(1))
            break

    # Packet loss rate (Kb)
    pattern = "\[\s*\d\] \d+.\d+-\d+.\d+ sec\s*\d+.\d+ \wBytes\s*\d+.\d+ Kbits\/sec\s*\d+.\d+ ms\s*\d+\/\s*\d+\s*\((\d+|\d+.\d+)%\)"
    for i, line in enumerate(open(senderLogFile, 'r')):
        if (re.match(pattern, line)):
            packetlossrate = float(re.match(pattern, line).group(1))
            break

    # RSSI
    pattern = "Signal strength:\s*-(\d+) dBm"
    rssi = 0.0
    for i, line in enumerate(open(senderLogFile, 'r')):
        if (re.match(pattern, line)):
            rssi = float(re.match(pattern, line).group(1)) * -1.0
            break

    # SNR
    pattern = "SNR:\s*(\d+) dB"
    snr = 0.0
    for i, line in enumerate(open(senderLogFile, 'r')):
        if (re.match(pattern, line)):
            snr = float(re.match(pattern, line).group(1))
            break

    # Throughput List
    throughputList = []
    pattern1 = "\[ \s*\d+\]\s*\d+\.\d+\-\d+\.\d+\s*\w*\s*(\d+|\d+\.\d+)\s*\w*\s*(\d+|\d+\.\d+)\s*Kbits\/\w*"
    pattern2 = "\[ \s*\d+\]\s*\d+\.\d+\-\d+\.\d+\s*\w*\s*(\d+|\d+\.\d+)\s*\w*\s*(\d+|\d+\.\d+)\s*Mbits\/\w*"
    for i, line in enumerate(open(senderLogFile, 'r')):
        if (re.match(pattern1, line)):
            throughputList.append(float(re.match(pattern1, line).group(2)))
        elif (re.match(pattern2, line)):
            throughputList.append(
                float(re.match(pattern2, line).group(2))*1000.0)

    return throughputList, latency, packetlossrate, rssi, snr


def draw_compare_line(expNumber):
    
    # 1
    ThroughputList1 = []
    LatencyList1 = []
    packetLossList1 = []
    RssiList1 = []
    SnrList1 = []
    for i in range(expNumber + 1):
        t, l, p, r, s = parse_log_from_file(logFolderName1 + senderLogFileName + "_" + str(
            i) + ".log")

        ThroughputList1.append(sum(t) / len(t))
        LatencyList1.append(l)
        packetLossList1.append(p)
        RssiList1.append(r)
        SnrList1.append(s)
        
        
    # 2
    ThroughputList2 = []
    LatencyList2 = []
    packetLossList2 = []
    RssiList2 = []
    SnrList2 = []
    for i in range(expNumber + 1):
        t, l, p, r, s = parse_log_from_file(logFolderName2 + senderLogFileName + "_" + str(
            i) + ".log")
        ThroughputList2.append(sum(t) / len(t))
        LatencyList2.append(l)
        packetLossList2.append(p)
        RssiList2.append(r)
        SnrList2.append(s)

    # 3
    ThroughputList3 = []
    LatencyList3 = []
    packetLossList3 = []
    RssiList3 = []
    SnrList3 = []
    for i in range(expNumber + 1):
        t, l, p, r, s = parse_log_from_file(logFolderName3 + senderLogFileName + "_" + str(
            i) + ".log")
        ThroughputList3.append(sum(t) / len(t))
        LatencyList3.append(l)
        packetLossList3.append(p)
        RssiList3.append(r)
        SnrList3.append(s)



    # Draw Fig
    colors = ["blue", "red", "green", 'purple', 'brown']
    labels = ["20", "30", "40"]
    x = [0, 1, 2]
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    # Throughput
    ThroughputList = pd.DataFrame({"1":ThroughputList1})
    ThroughputList["3"] = ThroughputList2
    ThroughputList["5"] = ThroughputList3


    
        
    sns.barplot(data=ThroughputList,errorbar=('ci', 95), errwidth=10, width=width)
    plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    plt.ylabel("Throughput (kbps)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    
    plt.savefig(figFolder + compare + "throughput_depth_wifi.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + compare + "throughput_depth_wifi.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()
    
    # Latency
    LatencyList = pd.DataFrame({"1": LatencyList1})
    LatencyList["3"] = LatencyList2
    LatencyList["5"] = LatencyList3


    sns.barplot(data=LatencyList,  errorbar=('ci', 95),
                  errwidth=10, width=width)
    plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    plt.ylabel("RTT (ms)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder +compare + "rtt_depth_wifi.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + compare + "rtt_depth_wifi.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()
    
    # Packet loss rate
    packetLossList = pd.DataFrame({"1": packetLossList1})
    packetLossList["3"] = packetLossList2
    packetLossList["5"] = packetLossList3

    sns.barplot(data=packetLossList,  errorbar=('ci', 95),
                  errwidth=10, width=width)
    plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    plt.ylabel("Packet Loss Rate (%)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + compare + "packetlossrate_depth_wifi.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + compare + "packetlossrate_depth_wifi.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()
    
    # RSSI
    RssiList = pd.DataFrame({"1": RssiList1})
    RssiList["3"] = RssiList2
    RssiList["5"] = RssiList3


    sns.barplot(data=RssiList,  errorbar=('ci', 95),
                  errwidth=10, width=width)
    plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    plt.ylabel("RSSI (dBm)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + compare + "rssi_depth_wifi.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + compare + "rssi_depth_wifi.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()
    
    

if __name__ == "__main__":
    

    
    
    # Args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--expNumber", type=int, default=0)
    args = parser.parse_args()
    
    draw_compare_line(args.expNumber)