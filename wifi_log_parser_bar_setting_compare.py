from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd
import matplotlib.ticker as ticker
import re

logFolderName1 = "fishtank_20cm_dry_sand_M31_6pm/T1_"
logFolderName2 = "fishtank_20cm_dry_sand_M31_6pm/T3_"
logFolderName3 = "fishtank_20cm_dry_sand_M31_6pm/T5_"
logFolderName4 = "fishtank_20cm_dry_sand_M31_6pm/T10_"
logFolderName5 = "fishtank_20cm_dry_sand_M31_6pm/T20_"
senderLogFileName = "wifi_send"
figFolder = "fig/fishtank_20cm_dry_sand_M31_6pm/wifi/"

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
    
    ThroughputList2[0] = ThroughputList2[1]

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
        
    

    # 4
    ThroughputList4 = []
    LatencyList4 = []
    packetLossList4 = []
    RssiList4 = []
    SnrList4 = []
    for i in range(expNumber + 1):
        t, l, p, r, s = parse_log_from_file(logFolderName4 + senderLogFileName + "_" + str(
            i) + ".log")
        ThroughputList4.append(sum(t) / len(t))
        LatencyList4.append(l)
        packetLossList4.append(p)
        RssiList4.append(r)
        SnrList4.append(s)
        


    # 5
    ThroughputList5 = []
    LatencyList5 = []
    packetLossList5 = []
    RssiList5 = []
    SnrList5 = []
    for i in range(expNumber + 1):
        t, l, p, r, s = parse_log_from_file(logFolderName5 + senderLogFileName + "_" + str(
            i) + ".log")
        ThroughputList5.append(sum(t) / len(t))
        LatencyList5.append(l)
        packetLossList5.append(p)
        RssiList5.append(r)
        SnrList5.append(s)


    # Draw Fig
    colors = "blue"

    labels = ["1", "3", "5", "10", "20"]
    x = [0, 1, 2, 3, 4]
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    # Throughput
    ThroughputList = pd.DataFrame({"1": ThroughputList1})
    ThroughputList["3"] = ThroughputList2
    ThroughputList["5"] = ThroughputList3
    ThroughputList["10"] = ThroughputList4
    ThroughputList["20"] = ThroughputList5
    
    sns.barplot(data=ThroughputList, errorbar=(
        'ci', 95), width=width, color=colors, errwidth=20)
    plt.xlabel("TX Power (dBm)", fontsize=my_fontsize)
    plt.ylabel("Throughput (kbps)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.tight_layout()
    plt.savefig(figFolder + "throughput_txpower_wifi.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "throughput_txpower_wifi.eps", dpi=300, bbox_inches="tight")
    plt.clf()
    
    # Latency
    LatencyList = pd.DataFrame({"1": LatencyList1})
    LatencyList["3"] = LatencyList2
    LatencyList["5"] = LatencyList3
    LatencyList["10"] = LatencyList4
    LatencyList["20"] = LatencyList5

    sns.barplot(data=LatencyList,  errorbar=('ci', 95),
                errwidth=20, width=width, color=colors)
    plt.xlabel("TX Power (dBm)", fontsize=my_fontsize)
    plt.ylabel("RTT (ms)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.tight_layout()
    plt.savefig(figFolder + "rtt_txpower_wifi.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "rtt_txpower_wifi.eps", dpi=300, bbox_inches="tight")
    plt.clf()
    
    # Packet loss rate
    packetLossList = pd.DataFrame({"1": packetLossList1})
    packetLossList["3"] = packetLossList2
    packetLossList["5"] = packetLossList3
    packetLossList["10"] = packetLossList4
    packetLossList["20"] = packetLossList5
    

    sns.barplot(data=packetLossList,  errorbar=('ci', 95),
                errwidth=20, width=width, color=colors)
    plt.xlabel("TX Power (dBm)", fontsize=my_fontsize)
    plt.ylabel("Packet Loss Rate (%)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.tight_layout()
    plt.savefig(figFolder + "packetlossrate_txpower_wifi.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "packetlossrate_txpower_wifi.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()
    
    # RSSI
    RssiList = pd.DataFrame({"1": RssiList1})
    RssiList["3"] = RssiList2
    RssiList["5"] = RssiList3
    RssiList["10"] = RssiList4
    RssiList["20"] = RssiList5

    sns.barplot(data=RssiList,  errorbar=('ci', 95),
                errwidth=20, width=width, color=colors)
    plt.xlabel("TX Power (dBm)", fontsize=my_fontsize)
    plt.ylabel("RSSI (dBm)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.tight_layout()
    plt.savefig(figFolder + "rssi_txpower_wifi.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "rssi_txpower_wifi.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()
    
    

if __name__ == "__main__":
    

    
    
    # Args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--expNumber", type=int, default=0)
    args = parser.parse_args()
    
    draw_compare_line(args.expNumber)