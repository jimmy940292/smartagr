from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd
import matplotlib.ticker as ticker
import re

logFolderName1 = "results/D10_B20_S1_M29/"
logFolderName2 = "results/D20_B20_S1_M29/"
logFolderName3 = "results/D40_B20_S1_M29/"
logFolderName4 = "results/D80_B20_S1_M29/"
logFolderName5 = "results/D160_B20_S1_M29/"
senderLogFileName = "wifi_send"
figFolder = "fig/M29/compare/wifi/"

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

    return throughput, latency, packetlossrate, rssi, snr


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

        ThroughputList1.append(t)
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
        ThroughputList2.append(t)
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
        ThroughputList3.append(t)
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
        ThroughputList4.append(t)
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
        ThroughputList5.append(t)
        LatencyList5.append(l)
        packetLossList5.append(p)
        RssiList5.append(r)
        SnrList5.append(s)

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
    ThroughputList = pd.DataFrame({"10cm":ThroughputList1})
    ThroughputList["20cm"] = ThroughputList2
    ThroughputList["40cm"] = ThroughputList3
    ThroughputList["80cm"] = ThroughputList4
    ThroughputList["160cm"] = ThroughputList5
        
    sns.pointplot(data=ThroughputList,  errorbar=('ci', 95), errwidth=10, scale=2, dodge=1, join=True)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("Throughput (kbps)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + "throughput_distance_wifi.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "throughput_distance_wifi.eps", dpi=300, bbox_inches="tight")
    plt.clf()
    
    # Latency
    LatencyList = pd.DataFrame({"10cm": LatencyList1})
    LatencyList["20cm"] = LatencyList2
    LatencyList["40cm"] = LatencyList3
    LatencyList["80cm"] = LatencyList4
    LatencyList["160cm"] = LatencyList5

    sns.pointplot(data=LatencyList,  errorbar=('ci', 95),
                  errwidth=10, scale=2, dodge=1, join=True)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("RTT (ms)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + "rtt_distance_wifi.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "rtt_distance_wifi.eps", dpi=300, bbox_inches="tight")
    plt.clf()
    
    # Packet loss rate
    packetLossList = pd.DataFrame({"10cm": packetLossList1})
    packetLossList["20cm"] = packetLossList2
    packetLossList["40cm"] = packetLossList3
    packetLossList["80cm"] = packetLossList4
    packetLossList["160cm"] = packetLossList5

    sns.pointplot(data=packetLossList,  errorbar=('ci', 95),
                  errwidth=10, scale=2, dodge=1, join=True)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("Packet Loss Rate (%)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + "packetlossrate_distance_wifi.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "packetlossrate_distance_wifi.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()
    
    # RSSI
    RssiList = pd.DataFrame({"10cm": RssiList1})
    RssiList["20cm"] = RssiList2
    RssiList["40cm"] = RssiList3
    RssiList["80cm"] = RssiList4
    RssiList["160cm"] = RssiList5

    sns.pointplot(data=RssiList,  errorbar=('ci', 95),
                  errwidth=10, scale=2, dodge=1, join=True)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("RSSI (dBm)", fontsize=my_fontsize)
    plt.xticks(x, labels, fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.savefig(figFolder + "rssi_distance_wifi.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "rssi_distance_wifi.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()
    
    

if __name__ == "__main__":
    

    
    
    # Args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--expNumber", type=int, default=0)
    args = parser.parse_args()
    
    draw_compare_line(args.expNumber)