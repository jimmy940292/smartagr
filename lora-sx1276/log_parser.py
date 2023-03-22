from datetime import datetime


logFolderName = "log/"
senderLogFileName = "lora_send.log"
receiverLogFileName = "lora_recv.log"

class PacketLog():
    
    def __init__(self):
        self.seq = 0
        self.packetSize = 0
        self.timeStamp = 0
        self.rssi = 0
        self.snr = 0


if __name__ == "__main__":
    
    # Open log files
    senderLogFile = open(logFolderName + senderLogFileName, "r")
    receiverLogFile = open(logFolderName + receiverLogFileName, "r")
    
    
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
    
    print("Avg Throughput: {} kbps".format(avgThroughput))
    print("Avg Latency: {} ms".format(avgLatency))
    print("Packet Loss Rate: {} %".format(packetLoss))
    print("Avg RSSI: {}".format(avgRssi))
    print("Avg SNR: {}".format(avgSnr))
    
    
    senderLogFile.close()
    receiverLogFile.close()
            
            
            