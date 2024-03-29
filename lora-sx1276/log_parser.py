from datetime import datetime
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import pandas as pd


logFolderName = "log/"
senderLogFileName = "lora_send"
receiverLogFileName = "lora_recv"

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
        if(receivePacket[recvIndex].seq != sendPacket[i].seq):
            lostPacket += (receivePacket[recvIndex].seq - sendPacket[i].seq)
            i = recvIndex - 1
            continue
        else:
            t1 = datetime.fromtimestamp(sendPacket[i].timeStamp)
            t2 = datetime.fromtimestamp(receivePacket[recvIndex].timeStamp)
            delta = (t2 - t1).total_seconds() * 1000.0
            throughputList.append(receivePacket[recvIndex].packetSize * 8.0 / 1000.0/ delta *1000.0) # kbps
            latencyList.append(delta) # ms
            rssiList.append(receivePacket[recvIndex].rssi)
            snrList.append(receivePacket[recvIndex].snr)
            
            
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
    
    
    senderLogFile.close()
    receiverLogFile.close()
    
    
    return avgThroughput, avgLatency, packetLoss, avgRssi, avgSnr
    
def draw_avg(senderLogFiles, receiverLogFiles):

    avgThroughputList = []
    avgLatencyList = []
    packetLossList = []
    avgRssiList = []
    avgSnr = []
    
    for i in range(len(senderLogFiles)):
        t, l, p, r, s = cal_avg_metric(senderLogFiles[i], receiverLogFiles[i], False)
        avgThroughputList.append(t)
        avgLatencyList.append(l)
        packetLossList.append(p)
        avgRssiList.append(r)
        avgSnr.append(s)
        
    # Draw Fig
    figFolder = "fig/"
    
    # Throughput
    avgThroughputList = np.array(avgThroughputList)
    avgThroughputList = np.reshape(avgThroughputList, (1, len(avgThroughputList)))
    avgThroughputList = pd.DataFrame(avgThroughputList)
    plot_throughput = sns.barplot(data=avgThroughputList)
    plt.xlabel("Exp Number")
    plt.ylabel("Throughput (kbps)")
    plot_throughput = plot_throughput.get_figure()
    plot_throughput.savefig(figFolder + "throughput.png")
    plt.show()
    
    # Latency
    
    # Packet loss rate
    
    # RSSI
    
    # SNR
        
    
    
    
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
        draw_avg(senderLogFiles, receiverLogFiles)            
    else:
        # Open log files
        senderLogFile = open(logFolderName + senderLogFileName + "_" + str(args.expNumber) + ".log", "r")
        receiverLogFile = open(logFolderName + receiverLogFileName + "_" + str(args.expNumber) + ".log", "r")
        cal_avg_metric(senderLogFile, receiverLogFile)
            
            
    
    
    
    
    
            
            
            