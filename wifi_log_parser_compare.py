from datetime import datetime
from functools import partial
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd
import matplotlib.ticker as ticker
import re

logFolderNames = ["rock/rock_20/T20_", "rock/rock_30/T20_", 
                  "rock/rock_40/T20_"]
# logFolderNames = ["fishtank_20cm_dry_sand_M31_6pm/T20_", "fishtank_20cm_300cc_sand_M31_7pm/T20_",
#                   "fishtank_20cm_600cc_sand_M31_7pm/T20_", "fishtank_20cm_1200cc_sand_M31_7pm/T20_", "fishtank_20cm_2400cc_sand_M31_7pm/T20_"]
senderLogFileName = "wifi_send"
figFolder = "fig/depth_compare/wifi/"
# figFolder = "fig/moisture_compare/wifi/"

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
    pattern = "\[\s*\d\] \d+\.\d+\-\d+\.\d+ sec\s*(\d+\.\d+|\d+) \wBytes\s*(\d+) Kbits\/sec\s*\d+.\d+ ms\s*\d+\/\s*\d+ \(\d+|\d+\.\d+%\)"
    for i, line in enumerate(open(senderLogFile, 'r')):
        if (re.match(pattern, line)):
            throughput = float(re.match(pattern, line).group(2))
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

    return throughput, latency, packetlossrate, rssi, snr

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
        for j in range(expNumber+1) :
            _t, _l, _p, _r, _s = parse_log_from_file(folderName + senderLogFileName + "_" + str(j) + ".log")
            t.append(_t)
            l.append(_l)
            p.append(_p)
            r.append(_r)
            s.append(_s)
            avgt += _t
            avgl += _l
            avgp += _p
            avgr += _r
            avgs += _s
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
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    # Throughput

    ThroughputList_err = []
    for i in range(len(ThroughputList)):
        ThroughputList_err.append(1.96*np.std(ThroughputList[i]) / np.sqrt(len(ThroughputList[i])))
    # sem = np.std(ThroughputList) / np.sqrt(len(ThroughputList))
    # z_score = 1.96
    # ThroughputList_err = z_score * sem
  
    plt.errorbar(x, avgThroughputList, yerr=ThroughputList_err, linewidth=10)

    x_major_locator = ticker.MultipleLocator(600)    
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    # sns.pointplot(x = np.arange(0, 5), y = ThroughputList, errorbar=('ci', 95), scale=2, dodge=1, join=True)
    plt.xlabel("Water (ml)", fontsize=my_fontsize)
    plt.ylabel("Throughput (kbps)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(-100, 2500)
    plt.tight_layout()
    plt.savefig(figFolder + "throughput_moisture_wifi.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "throughput_moisture_wifi.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    # Latency
    LatencyList_err = []
    for i in range(len(LatencyList)):
        LatencyList_err.append(
            1.96*np.std(LatencyList[i]) / np.sqrt(len(LatencyList[i])))
    # sem = np.std(LatencyList) / np.sqrt(len(LatencyList))
    # z_score = 1.96
    # LatencyList_err = z_score * sem
    plt.errorbar(x, avgLatencyList, yerr=LatencyList_err, linewidth=10)

    x_major_locator = ticker.MultipleLocator(600)    
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    plt.xlabel("Water (ml)", fontsize=my_fontsize)
    plt.ylabel("Latency (ms)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(-100, 2500)
    plt.tight_layout()
    plt.savefig(figFolder + "latency_moisture_wifi.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "latency_moisture_wifi.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    # PacketLoss
    PacketLossList_err = []
    for i in range(len(PacketLossList)):
        PacketLossList_err.append(
            1.96*np.std(PacketLossList[i]) / np.sqrt(len(PacketLossList[i])))
    # sem = abs(np.std(PacketLossList) / np.sqrt(len(PacketLossList)))
    # print(sem)
    # z_score = 1.96
    # PacketLossList_err = z_score * sem
    plt.errorbar(x, avgPacketLossList, yerr = PacketLossList_err, linewidth=10)

    x_major_locator = ticker.MultipleLocator(600)
    y_major_locator = ticker.MultipleLocator(0.1)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    axes.yaxis.set_major_locator(y_major_locator)
    plt.xlabel("Water (ml)", fontsize=my_fontsize)
    plt.ylabel("Packet Loss Rate (%)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    # plt.yticks(fontsize=my_fontsize)
    plt.xlim(-100, 2500)
    plt.yticks(plt.yticks()[0], [
        f'{x:.1f}' for x in plt.yticks()[0]], fontsize=my_fontsize)
    plt.ylim(0)
    plt.tight_layout()
    plt.savefig(figFolder + "packetLoss_moisture_wifi.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "packetLoss_moisture_wifi.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    # Rssi
    RssiList_err = []
    for i in range(len(RssiList)):
        RssiList_err.append(
            1.96*np.std(RssiList[i]) / np.sqrt(len(RssiList[i])))
    # sem = np.std(RssiList) / np.sqrt(len(RssiList))
    # z_score = 1.96
    # RssiList_err = z_score * sem
    plt.errorbar(x, avgRssiList, yerr = RssiList_err, linewidth=10)

    x_major_locator = ticker.MultipleLocator(600)    
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    plt.xlabel("Water (ml)", fontsize=my_fontsize)
    plt.ylabel("RSSI (dBm)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(-100, 2500)
    plt.tight_layout()
    plt.savefig(figFolder + "rssi_moisture_wifi.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "rssi_moisture_wifi.eps", dpi=300, bbox_inches="tight")
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
        for j in range(expNumber+1):
            _t, _l, _p, _r, _s = parse_log_from_file(
                folderName + senderLogFileName + "_" + str(j) + ".log")
            t.append(_t)
            l.append(_l)
            p.append(_p)
            r.append(_r)
            s.append(_s)
            avgt += _t
            avgl += _l
            avgp += _p
            avgr += _r
            avgs += _s
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
    x = [10, 20, 40, 80, 160]
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    # Throughput
    sem = np.std(ThroughputList) / np.sqrt(len(ThroughputList))
    z_score = 1.96
    ThroughputList_err = z_score * sem
    plt.errorbar(x, ThroughputList, yerr = ThroughputList_err, linewidth=10)

    x_major_locator = ticker.MultipleLocator(50)    
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    # sns.pointplot(x = np.arange(0, 5), y = ThroughputList, errorbar=('ci', 95), scale=2, dodge=1, join=True)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("Throughput (kbps)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 200)
    plt.savefig(figFolder + "throughput_distance_wifi.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "throughput_distance_wifi.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    # Latency
    sem = np.std(LatencyList) / np.sqrt(len(LatencyList))
    z_score = 1.96
    LatencyList_err = z_score * sem
    plt.errorbar(x, LatencyList, yerr = LatencyList_err, linewidth=10)

    x_major_locator = ticker.MultipleLocator(50)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("Latency (ms)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 200)
    plt.savefig(figFolder + "latency_distance_wifi.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "latency_distance_wifi.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    # PacketLoss
    sem = np.std(PacketLossList) / np.sqrt(len(PacketLossList))
    z_score = 1.96
    PacketLossList_err = z_score * sem
    plt.errorbar(x, PacketLossList, yerr = PacketLossList_err, linewidth=10)

    x_major_locator = ticker.MultipleLocator(50)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("Packet Loss Rate (%)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 200)
    plt.ylim(0)
    plt.savefig(figFolder + "packetLoss_distance_wifi.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "packetLoss_distance_wifi.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    # Rssi
    sem = np.std(RssiList) / np.sqrt(len(RssiList))
    z_score = 1.96
    RssiList_err = z_score * sem
    plt.errorbar(x, RssiList, yerr = RssiList_err, linewidth=10)

    x_major_locator = ticker.MultipleLocator(50)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("RSSI (dBm)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 200)
    plt.savefig(figFolder + "rssi_distance_wifi.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "rssi_distance_wifi.eps", dpi=300, bbox_inches="tight")
    plt.clf()

    sem = np.std(SnrList) / np.sqrt(len(SnrList))
    z_score = 1.96
    SnrList_err = z_score * sem
    plt.errorbar(x, SnrList, yerr = SnrList_err, linewidth=10)

    x_major_locator = ticker.MultipleLocator(50)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    plt.xlabel("Distance (cm)", fontsize=my_fontsize)
    plt.ylabel("SNR (dB)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 200)
    plt.savefig(figFolder + "snr_distance_wifi.svg", dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "snr_distance_wifi.eps", dpi=300, bbox_inches="tight")
    plt.clf()
    

def draw_depth_line(expNumber):
    ThroughputList = []
    LatencyList = []
    PacketLossList = []
    RssiList = []
    SnrList = []
    for i in range(len(logFolderNames)):
        folderName = logFolderNames[i]
        avgt = 0
        avgl = 0
        avgp = 0
        avgr = 0
        avgs = 0
        for j in range(expNumber+1):
            _t, _l, _p, _r, _s = parse_log_from_file(
                folderName + senderLogFileName + "_" + str(j) + ".log")
            avgt += _t
            avgl += _l
            avgp += _p
            avgr += _r
            avgs += _s
        avgt /= (expNumber+1)
        avgl /= (expNumber+1)
        avgp /= (expNumber+1)
        avgr /= (expNumber+1)
        avgs /= (expNumber+1)
        ThroughputList.append(avgt)
        LatencyList.append(avgl)
        PacketLossList.append(avgp)
        RssiList.append(avgr)
        SnrList.append(avgs)

    colors = ["blue", "red", "green", 'purple', 'brown']
    labels = ["20", "30", "40"]
    x = [20, 30, 40]
    z= [4000]*len(ThroughputList)
    plt.figure(figsize=my_figsize, dpi=100, linewidth=1)
    plt.rcParams['font.family'] = 'DeJavu Serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    # Throughput
    # sem = abs(np.std(ThroughputList) / np.sqrt(len(ThroughputList)))
    # z_score = 1.96
    # ThroughputList_err = z_score * sem
    print(ThroughputList)
    plt.plot(x, ThroughputList , linewidth=20)
    plt.scatter(x, ThroughputList, s=z, marker="o")

    x_major_locator = ticker.MultipleLocator(10)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    # sns.pointplot(x = np.arange(0, 5), y = ThroughputList, errorbar=('ci', 95), scale=2, dodge=1, join=True)
    plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    plt.ylabel("Throughput (kbps)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 50)
    plt.tight_layout()
    plt.savefig(figFolder + "throughput_depth_wifi.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "throughput_depth_wifi.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # Latency
    # sem = abs(np.std(LatencyList) / np.sqrt(len(LatencyList)))
    # z_score = 1.96
    # LatencyList_err = z_score * sem
    plt.plot(x, LatencyList,  linewidth=20)
    plt.scatter(x, LatencyList, s=z, marker="o")
    x_major_locator = ticker.MultipleLocator(10)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    plt.ylabel("RTT (ms)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 50)
    plt.tight_layout()
    plt.savefig(figFolder + "latency_depth_wifi.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "latency_depth_wifi.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # PacketLoss
    # sem = abs(np.std(PacketLossList) / np.sqrt(len(PacketLossList)))
    # z_score = 1.96
    # PacketLossList_err = z_score * sem
    plt.plot(x, PacketLossList,  linewidth=20)
    plt.scatter(x, PacketLossList, s=z, marker="o")
    x_major_locator = ticker.MultipleLocator(10)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    plt.ylabel("Packet Loss Rate (%)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 50)
    plt.ylim(0)
    plt.tight_layout()
    plt.savefig(figFolder + "packetLoss_depth_wifi.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "packetLoss_depth_wifi.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # Rssi
    # sem = abs(np.std(RssiList) / np.sqrt(len(RssiList)))
    # z_score = 1.96
    # RssiList_err = z_score * sem
    plt.plot(x, RssiList,  linewidth=20)
    plt.scatter(x, RssiList, s=z, marker="o")
    x_major_locator = ticker.MultipleLocator(10)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    plt.ylabel("RSSI (dBm)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 50)
    plt.tight_layout()
    plt.savefig(figFolder + "rssi_depth_wifi.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "rssi_depth_wifi.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    # sem = abs(np.std(SnrList) / np.sqrt(len(SnrList)))
    # z_score = 1.96
    # SnrList_err = z_score * sem
    plt.plot(x, SnrList,  linewidth=20)
    plt.scatter(x, SnrList, s=z, marker="o")
    x_major_locator = ticker.MultipleLocator(10)
    axes = plt.gca()
    axes.xaxis.set_major_locator(x_major_locator)
    plt.xlabel("Depth (cm)", fontsize=my_fontsize)
    plt.ylabel("SNR (dB)", fontsize=my_fontsize)
    # plt.xscale('function', functions=(partial(np.power, 2.0), np.log2))
    plt.xticks(fontsize=my_fontsize)
    plt.yticks(fontsize=my_fontsize)
    plt.xlim(0, 50)
    plt.tight_layout()
    plt.savefig(figFolder + "snr_depth_wifi.svg",
                dpi=300, bbox_inches="tight")
    plt.savefig(figFolder + "snr_depth_wifi.eps",
                dpi=300, bbox_inches="tight")
    plt.clf()

    
    

if __name__ == "__main__":
    

    
    
    # Args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--expNumber", type=int, default=0)
    args = parser.parse_args()
    
    # draw_moisture_line(args.expNumber)
    draw_depth_line(args.expNumber)