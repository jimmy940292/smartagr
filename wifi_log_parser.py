from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd
import re
import matplotlib.ticker as ticker


logFolderName = "example_data/"
senderLogFileName = "wifi_send"




def parse_log_from_file(senderLogFile):
    
    
    
    # Throughput (Mb)
    pattern = "\[\s*\d\] \d+.\d+-\d+.\d+ sec\s*\d+.\d+ MBytes\s*(\d+.\d+) Mbits\/sec\s*\d+.\d+ ms\s*\d+\/\s*\d+ \([\d]+|[\d+.\d+]%\)"
    throughput = 0.0
    for i, line in enumerate(open(senderLogFile, 'r')):
        if(re.match(pattern, line)):
            throughput = float(re.match(pattern, line).group(1))
            throughput *= 1000
            break
        
    # Throughput (Kb)
    pattern = "\[\s*\d\] \d+\.\d+\-\d+\.\d+ sec\s*\d+\.\d+ KBytes\s*(\d+) Kbits/sec\s*\d+.\d+ ms\s*\d+\/\s*\d+ \([\d]+|[\d+.\d+]%\)"
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
    pattern = "\[\s*\d\] \d+.\d+-\d+.\d+ sec\s*\d+.\d+ MBytes\s*\d+.\d+ Mbits\/sec\s*\d+.\d+ ms\s*\d+\/\s*\d+ \(([\d]+|[\d+.\d+])%\)"
    packetlossrate = 0.0
    for i, line in enumerate(open(senderLogFile, 'r')):
        if (re.match(pattern, line)):
            packetlossrate = float(re.match(pattern, line).group(1))
            break
        
    # Packet loss rate (Kb)
    pattern = "\[\s*\d\] \d+.\d+-\d+.\d+ sec\s*\d+.\d+ KBytes\s*\d+.\d+ Kbits\/sec\s*\d+.\d+ ms\s*\d+\/\s*\d+ \(([\d]+|[\d+.\d+])%\)"
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
    
    
def draw_avg_bar(senderLogFiles):

    avgThroughputList = []
    avgLatencyList = []
    packetLossList = []
    avgRssiList = []
    avgSnr = []

    for i in range(len(senderLogFiles)):
        t, l, p, r, s = parse_log_from_file(senderLogFiles[i])
        avgThroughputList.append(t)
        avgLatencyList.append(l)
        packetLossList.append(p)
        avgRssiList.append(r)
        avgSnr.append(s)

    # Draw Fig
    figFolder = "fig/wifi/"

    # Throughput
    avgThroughputList = np.array(avgThroughputList)
    avgThroughputList = np.reshape(
        avgThroughputList, (1, len(avgThroughputList)))
    avgThroughputList = pd.DataFrame(avgThroughputList)
    plot_throughput = sns.barplot(data=avgThroughputList)
    plt.xlabel("Exp Number")
    plt.ylabel("Throughput (kbps)")
    plot_throughput = plot_throughput.get_figure()
    plot_throughput.savefig(figFolder + "throughput_bar.png")
    plt.show()

    # Latency
    avgLatencyList = np.array(avgLatencyList)
    avgLatencyList = np.reshape(avgLatencyList, (1, len(avgLatencyList)))
    avgLatencyList = pd.DataFrame(avgLatencyList)
    plot_latency = sns.barplot(data=avgLatencyList)
    plt.xlabel("Exp Number")
    plt.ylabel("Latency (ms)")
    plot_latency = plot_latency.get_figure()
    plot_latency.savefig(figFolder + "latency_bar.png")
    plt.show()

    # Packet loss rate
    packetLossList = np.array(packetLossList)
    packetLossList = np.reshape(packetLossList, (1, len(packetLossList)))
    packetLossList = pd.DataFrame(packetLossList)
    plot_packetloss = sns.barplot(data=packetLossList)
    plt.xlabel("Exp Number")
    plt.ylabel("Packet loss rate (%)")
    plot_packetloss = plot_packetloss.get_figure()
    plot_packetloss.savefig(figFolder + "packetlossrate_bar.png")
    plt.show()

    # SNR
    avgSnr = np.array(avgSnr)
    avgSnr = np.reshape(avgSnr, (1, len(avgSnr)))
    avgSnr = pd.DataFrame(avgSnr)
    plot_snr = sns.barplot(data=avgSnr)
    plt.xlabel("Exp Number")
    plt.ylabel("SNR (dB)")
    plot_snr = plot_snr.get_figure()
    plot_snr.savefig(figFolder + "snr_bar.png")
    plt.show()

    # RSSI
    avgRssiList = np.array(avgRssiList)
    newRssiList = avgRssiList
    avgRssiList = np.reshape(avgRssiList, (1, len(avgRssiList)))
    avgRssiList = pd.DataFrame(avgRssiList)
    plot_rssi = sns.barplot(data=avgRssiList)
    plt.xlabel("Exp Number")
    plt.ylabel("RSSI (dBm)")
    plt.ylim(min(newRssiList), 0)
    plot_rssi = plot_rssi.get_figure()
    plot_rssi.savefig(figFolder + "rssi_bar.png")
    plt.show()
    

def draw_avg_line(senderLogFiles):

    avgThroughputList = []
    avgLatencyList = []
    packetLossList = []
    avgRssiList = []
    avgSnr = []

    for i in range(len(senderLogFiles)):
        t, l, p, r, s = parse_log_from_file(senderLogFiles[i])
        avgThroughputList.append(t)
        avgLatencyList.append(l)
        packetLossList.append(p)
        avgRssiList.append(r)
        avgSnr.append(s)

    # Draw Fig
    figFolder = "fig/wifi/"

    # Throughput
    avgThroughputList = np.array(avgThroughputList)
    avgThroughputList = pd.DataFrame({"Throughput": avgThroughputList})
    plot_throughput = sns.lineplot(
        y="Throughput", x=avgThroughputList.index, data=avgThroughputList, markers="o")
    plot_throughput.xaxis.set_major_locator(ticker.MultipleLocator(1))
    plot_throughput.xaxis.set_major_formatter(ticker.ScalarFormatter())
    plt.xlabel("Exp Number")
    plt.ylabel("Throughput (kbps)")
    plot_throughput = plot_throughput.get_figure()
    plot_throughput.savefig(figFolder + "throughput_line.png")
    plt.show()

    # Latency
    avgLatencyList = np.array(avgLatencyList)
    avgLatencyList = pd.DataFrame({"Latency": avgLatencyList})
    plot_latency = sns.lineplot(
        y="Latency", x=avgLatencyList.index, data=avgLatencyList, markers="o")
    plot_latency.xaxis.set_major_locator(ticker.MultipleLocator(1))
    plot_latency.xaxis.set_major_formatter(ticker.ScalarFormatter())
    plt.xlabel("Exp Number")
    plt.ylabel("Latency (ms)")
    plot_latency = plot_latency.get_figure()
    plot_latency.savefig(figFolder + "latency_line.png")
    plt.show()

    # Packet loss rate
    packetLossList = np.array(packetLossList)
    packetLossList = pd.DataFrame({"Packetlossrate": packetLossList})
    plot_packetloss = sns.lineplot(
        y="Packetlossrate", x=packetLossList.index, data=packetLossList, markers="o")
    plot_packetloss.xaxis.set_major_locator(ticker.MultipleLocator(1))
    plot_packetloss.xaxis.set_major_formatter(ticker.ScalarFormatter())
    plt.xlabel("Exp Number")
    plt.ylabel("Packet loss rate (%)")
    plot_packetloss = plot_packetloss.get_figure()
    plot_packetloss.savefig(figFolder + "packetlossrate_line.png")
    plt.show()

    # SNR
    avgSnr = np.array(avgSnr)
    avgSnr = pd.DataFrame({"SNR": avgSnr})
    plot_snr = sns.lineplot(y="SNR", x=avgSnr.index, data=avgSnr, markers="o")
    plot_snr.xaxis.set_major_locator(ticker.MultipleLocator(1))
    plot_snr.xaxis.set_major_formatter(ticker.ScalarFormatter())
    plt.xlabel("Exp Number")
    plt.ylabel("SNR (dB)")
    plot_snr = plot_snr.get_figure()
    plot_snr.savefig(figFolder + "snr_line.png")
    plt.show()

    # RSSI
    avgRssiList = np.array(avgRssiList)
    newRssiList = avgRssiList
    avgRssiList = pd.DataFrame({"RSSI": avgRssiList})
    plot_rssi = sns.lineplot(
        y="RSSI", x=avgRssiList.index, data=avgRssiList, markers="o")
    plot_rssi.xaxis.set_major_locator(ticker.MultipleLocator(1))
    plot_rssi.xaxis.set_major_formatter(ticker.ScalarFormatter())
    plt.xlabel("Exp Number")
    plt.ylabel("RSSI (dBm)")
    plt.ylim(min(newRssiList), max(newRssiList))
    plot_rssi = plot_rssi.get_figure()
    plot_rssi.savefig(figFolder + "rssi_line.png")
    plt.show()
    
    
    
if __name__ == "__main__":
    
    read_all_file = True
    
    
    # Args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--expNumber", type=int, default=0)
    args = parser.parse_args()
    senderLogFiles = []
    for i in range(args.expNumber + 1):
        s_file = logFolderName + senderLogFileName + "_" + str(i) + ".log"
        senderLogFiles.append(s_file)
    
    # Bar
    # draw_avg_bar(senderLogFiles)   
    
    # Line
    draw_avg_line(senderLogFiles)

            
            
    
    
    
    
    
            
            
            