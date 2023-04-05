import numpy as np
import pandas as pd
from datetime import datetime
import math
import re

dataFolder = "data/"


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

class PacketLog():

    def __init__(self):
        self.seq = 0
        self.packetSize = 0
        self.timeStamp = 0
        self.rssi = 0
        self.snr = 0


def cal_10s_metric(senderLogFile, receiverLogFile, doprint=True):
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

     # Calculate average metrics in 10s
    avgThroughput = []
    avgLatency = []
    avgRssi = []
    avgSnr = []
    packetLoss = []

    # last_t = datetime.fromtimestamp(
    #     receivePacket[len(receivePacket) - 1].timeStamp)
    # delta = (last_t - first_t).total_seconds() * 1000.0

    recvIndex = 0
    index = int(len(sendPacket) / 10)

    loss_list = []
    sent_size = 0
    first_t = datetime.fromtimestamp(receivePacket[0].timeStamp)
    for i in range(len(receivePacket)):
        diff_t = (datetime.fromtimestamp(
            receivePacket[i].timeStamp) - first_t).total_seconds()
        if (diff_t < 1.0):
            # print("diff_t {}", diff_t)
            sent_size += (receivePacket[i].packetSize * 8.0 / 1000.0)
        else:
            # print("sent_size = {}, diff_t = {}".format(sent_size, diff_t))
            avgThroughput.append(sent_size/diff_t)
            sent_size = (receivePacket[i].packetSize * 8.0 / 1000.0)
            first_t = datetime.fromtimestamp(receivePacket[i].timeStamp)
    diff_t = (datetime.fromtimestamp(
        receivePacket[0].timeStamp+10) - first_t).total_seconds()
    # print("sent_size = {}, diff_t = {}\n\n".format(sent_size, diff_t))
    avgThroughput.append(sent_size/diff_t)

    for i in range(len(sendPacket)):
        if (recvIndex >= len(receivePacket) or receivePacket[recvIndex].seq != sendPacket[i].seq):
            latencyList.append(0)  # ms
            rssiList.append(0)
            snrList.append(0)
            lostPacket += 1
        else:
            t1 = datetime.fromtimestamp(sendPacket[i].timeStamp)
            t2 = datetime.fromtimestamp(receivePacket[recvIndex].timeStamp)
            delta = (t2 - t1).total_seconds() * 1000.0
            # throughputList.append(
            #     receivePacket[recvIndex].packetSize * 8.0 / 1000.0 / delta * 1000.0)  # kbps
            # throughputList.append(
            #     receivePacket[recvIndex].packetSize * 8.0 / 1000.0)  # kbps
            latencyList.append(delta)  # ms
            rssiList.append(receivePacket[recvIndex].rssi)
            snrList.append(receivePacket[recvIndex].snr)
            recvIndex += 1
        if (i % index == 9):
            loss_list.append(lostPacket)
            lostPacket = 0

    # print("{} : {}".format(len(loss_list), len(sendPacket)))
    # print(loss_list)
    #     print(latencyList[i])
    l = len(avgThroughput)
    for i in range(l, 10):
        avgThroughput.append(0)

    for i in range(index):
        # avgThroughput.append(
        #     sum(throughputList[i*10:i*10+9]) / len(throughputList[i*10:i*10+9]) * 100.0)
        # avgThroughput.append(sum(throughputList[i*10:i*10+9]) * 10)
        sumLatency = 0
        validLatency = 0
        for j in range(i*10, (i+1)*10):
            if (latencyList[j] != 0):
                validLatency += 1
                sumLatency += latencyList[j]
        if (validLatency == 0):
            avgLatency.append(0)
        else:
            avgLatency.append(sumLatency / validLatency)

        sumRssi = 0
        validRssi = 0
        for j in range(i*10, (i+1)*10):
            if (rssiList[j] != 0):
                validRssi += 1
                sumRssi += rssiList[j]
        if (validRssi == 0):
            avgRssi.append(0)
        else:
            avgRssi.append(sumRssi / validRssi)

        sumSnr = 0
        validSnr = 0
        for j in range(i*10, (i+1)*10):
            if (snrList[j] != 0):
                validSnr += 1
                sumSnr += snrList[j]
        if (validSnr == 0):
            avgSnr.append(0)
        else:
            avgSnr.append(sumSnr / validSnr)
        packetLoss.append(
            (loss_list[i]) / len(sendPacket[i*10:(i+1)*10]) * 100.0)
        # if (len(latencyList[i*10:(i+1)*10]) > 0):
        #     avgLatency.append(
        #     sum(latencyList[i*10:(i+1)*10]) / len(latencyList[i*10:(i+1)*10]))
        # else:
        #     avgLatency.append(0)
        # if (len(rssiList[i*10:(i+1)*10]) > 0):
        #     avgRssi.append(sum(rssiList[i*10:(i+1)*10]) / len(rssiList[i*10:(i+1)*10]))
        # else:
        #     avgRssi.append(0)
        # if (len(snrList[i*10:(i+1)*10]) > 0):
        #     avgSnr.append(sum(snrList[i*10:(i+1)*10]) / len(snrList[i*10:(i+1)*10]))
        # else:
        #     avgSnr.append(0)
        # packetLoss.append(
        #     (loss_list[i]) / len(sendPacket[i*10:(i+1)*10]) * 100.0)

    senderLogFile.close()
    receiverLogFile.close()

    return np.array(avgThroughput), np.array(avgLatency), np.array(packetLoss), np.array(avgRssi), np.array(avgSnr)


def extract_avg_from_lora():
    # Lora

    # Distance

    df_lora = {"throughput (kbps)": [], "latency (ms)": [],
                   "packetlossrate (%)": [], "snr (dB)": [], "rssi (dBm)": [], "distance (cm)": [], "depth (cm)":[], "moisture (ml)": [],"soil type":[], "tx_power (dBm)":[], "datarate":[]}
    df_lora = pd.DataFrame(data=df_lora)

    

    # D10
    
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(12):

        _t, _l, _p, _r, _s = cal_10s_metric(open("results/D10_B20_S1_M29/" + "lora_send_" + str(
            i)+".log", "r"), open("results/D10_B20_S1_M29/" + "lora_recv_" + str(i)+".log", "r"))

        _t = sum(_t) / len(_t)
        _l = sum(_l) / len(_l)
        _p = sum(_p) / len(_p)
        _r = sum(_r) / len(_r)
        _s = sum(_s) / len(_s)
        t.append(_t)
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)

    df = {"throughput (kbps)": t, "latency (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 10, "depth (cm)": 20, "moisture (ml)": 0, "soil type": "yellow soil", "tx_power (dBm)": 15, "datarate": 4}
    df_lora = df_lora.append(df, ignore_index=True)

    # D20
    
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(12):

        _t, _l, _p, _r, _s = cal_10s_metric(open("results/D20_B20_S1_M29/" + "lora_send_" + str(
            i)+".log", "r"), open("results/D20_B20_S1_M29/" + "lora_recv_" + str(i)+".log", "r"))

        _t = sum(_t) / len(_t)
        _l = sum(_l) / len(_l)
        _p = sum(_p) / len(_p)
        _r = sum(_r) / len(_r)
        _s = sum(_s) / len(_s)
        t.append(_t)
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)

    df = {"throughput (kbps)": t, "latency (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 20, "depth (cm)": 20, "moisture (ml)": 0, "soil type": "yellow soil", "tx_power (dBm)": 15, "datarate": 4}
    df_lora = df_lora.append(df, ignore_index=True)
    
    # D40
    
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(12):

        _t, _l, _p, _r, _s = cal_10s_metric(open("results/D40_B20_S1_M29/" + "lora_send_" + str(
            i)+".log", "r"), open("results/D40_B20_S1_M29/" + "lora_recv_" + str(i)+".log", "r"))

        _t = sum(_t) / len(_t)
        _l = sum(_l) / len(_l)
        _p = sum(_p) / len(_p)
        _r = sum(_r) / len(_r)
        _s = sum(_s) / len(_s)
        t.append(_t)
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)

    df = {"throughput (kbps)": t, "latency (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 40, "depth (cm)": 20, "moisture (ml)": 0, "soil type": "yellow soil", "tx_power (dBm)": 15, "datarate": 4}
    df_lora = df_lora.append(df, ignore_index=True)
    
    # 80
    
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(12):

        _t, _l, _p, _r, _s = cal_10s_metric(open("results/D80_B20_S1_M29/" + "lora_send_" + str(
            i)+".log", "r"), open("results/D80_B20_S1_M29/" + "lora_recv_" + str(i)+".log", "r"))

        _t = sum(_t) / len(_t)
        _l = sum(_l) / len(_l)
        _p = sum(_p) / len(_p)
        _r = sum(_r) / len(_r)
        _s = sum(_s) / len(_s)
        t.append(_t)
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)

    df = {"throughput (kbps)": t, "latency (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 80, "depth (cm)": 20, "moisture (ml)": 0, "soil type": "yellow soil", "tx_power (dBm)": 15, "datarate": 4}
    df_lora = df_lora.append(df, ignore_index=True)
    
    # 160
    
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(12):

        _t, _l, _p, _r, _s = cal_10s_metric(open("results/D160_B20_S1_M29/" + "lora_send_" + str(
            i)+".log", "r"), open("results/D160_B20_S1_M29/" + "lora_recv_" + str(i)+".log", "r"))

        _t = sum(_t) / len(_t)
        _l = sum(_l) / len(_l)
        _p = sum(_p) / len(_p)
        _r = sum(_r) / len(_r)
        _s = sum(_s) / len(_s)
        t.append(_t)
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)

    df = {"throughput (kbps)": t, "latency (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 160, "depth (cm)": 20, "moisture (ml)": 0, "soil type": "yellow soil", "tx_power (dBm)": 15, "datarate": 4}
    df_lora = df_lora.append(df, ignore_index=True)
    
    # Dry Sand
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(6):

        _t, _l, _p, _r, _s = cal_10s_metric(open("fishtank_20cm_dry_sand_M31_6pm/" + "D4B500T15_lora_send_" + str(
            i)+".log", "r"), open("fishtank_20cm_dry_sand_M31_6pm/" + "D4B500T15_lora_recv_" + str(i)+".log", "r"))

        _t = sum(_t) / len(_t)
        _l = sum(_l) / len(_l)
        _p = sum(_p) / len(_p)
        _r = sum(_r) / len(_r)
        _s = sum(_s) / len(_s)
        t.append(_t)
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)

    df = {"throughput (kbps)": t, "latency (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 20, "depth (cm)": 20, "moisture (ml)": 0, "soil type": "sand", "tx_power (dBm)": 15, "datarate": 4}
    df_lora = df_lora.append(df, ignore_index=True)
    
    # 300 ml
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(3):

        _t, _l, _p, _r, _s = cal_10s_metric(open("fishtank_20cm_300cc_sand_M31_7pm/" + "D4B500T15_lora_send_" + str(
            i)+".log", "r"), open("fishtank_20cm_300cc_sand_M31_7pm/" + "D4B500T15_lora_recv_" + str(i)+".log", "r"))

        _t = sum(_t) / len(_t)
        _l = sum(_l) / len(_l)
        _p = sum(_p) / len(_p)
        _r = sum(_r) / len(_r)
        _s = sum(_s) / len(_s)
        t.append(_t)
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)

    df = {"throughput (kbps)": t, "latency (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 20, "depth (cm)": 20, "moisture (ml)": 300, "soil type": "sand", "tx_power (dBm)": 15, "datarate": 4}
    df_lora = df_lora.append(df, ignore_index=True)
    
    # 600 ml
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(3):

        _t, _l, _p, _r, _s = cal_10s_metric(open("fishtank_20cm_600cc_sand_M31_7pm/" + "D4B500T15_lora_send_" + str(
            i)+".log", "r"), open("fishtank_20cm_600cc_sand_M31_7pm/" + "D4B500T15_lora_recv_" + str(i)+".log", "r"))

        _t = sum(_t) / len(_t)
        _l = sum(_l) / len(_l)
        _p = sum(_p) / len(_p)
        _r = sum(_r) / len(_r)
        _s = sum(_s) / len(_s)
        t.append(_t)
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)

    df = {"throughput (kbps)": t, "latency (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 20, "depth (cm)": 20, "moisture (ml)": 600, "soil type": "sand", "tx_power (dBm)": 15, "datarate": 4}
    df_lora = df_lora.append(df, ignore_index=True)
    
    # 1200 ml
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(3):

        _t, _l, _p, _r, _s = cal_10s_metric(open("fishtank_20cm_1200cc_sand_M31_7pm/" + "D4B500T15_lora_send_" + str(
            i)+".log", "r"), open("fishtank_20cm_1200cc_sand_M31_7pm/" + "D4B500T15_lora_recv_" + str(i)+".log", "r"))

        _t = sum(_t) / len(_t)
        _l = sum(_l) / len(_l)
        _p = sum(_p) / len(_p)
        _r = sum(_r) / len(_r)
        _s = sum(_s) / len(_s)
        t.append(_t)
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)

    df = {"throughput (kbps)": t, "latency (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 20, "depth (cm)": 20, "moisture (ml)": 1200, "soil type": "sand", "tx_power (dBm)": 15, "datarate": 4}
    df_lora = df_lora.append(df, ignore_index=True)
    
    # 2400 ml
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(3):

        _t, _l, _p, _r, _s = cal_10s_metric(open("fishtank_20cm_2400cc_sand_M31_7pm/" + "D4B500T15_lora_send_" + str(
            i)+".log", "r"), open("fishtank_20cm_2400cc_sand_M31_7pm/" + "D4B500T15_lora_recv_" + str(i)+".log", "r"))

        _t = sum(_t) / len(_t)
        _l = sum(_l) / len(_l)
        _p = sum(_p) / len(_p)
        _r = sum(_r) / len(_r)
        _s = sum(_s) / len(_s)
        t.append(_t)
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)

    df = {"throughput (kbps)": t, "latency (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 20, "depth (cm)": 20, "moisture (ml)": 2400, "soil type": "sand", "tx_power (dBm)": 15, "datarate": 4}
    df_lora = df_lora.append(df, ignore_index=True)
    
    # Rock 20cm
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(1):

        _t, _l, _p, _r, _s = cal_10s_metric(open("rock/rock_20/" + "D4B500T15_lora_send_" + str(
            i)+".log", "r"), open("rock/rock_20/" + "D4B500T15_lora_recv_" + str(i)+".log", "r"))

        _t = sum(_t) / len(_t)
        _l = sum(_l) / len(_l)
        _p = sum(_p) / len(_p)
        _r = sum(_r) / len(_r)
        _s = sum(_s) / len(_s)
        t.append(_t)
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)

    df = {"throughput (kbps)": t, "latency (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 20, "depth (cm)": 20, "moisture (ml)": 0, "soil type": "gravel", "tx_power (dBm)": 15, "datarate": 4}
    df_lora = df_lora.append(df, ignore_index=True)
    
    # Rock 30cm
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(1):

        _t, _l, _p, _r, _s = cal_10s_metric(open("rock/rock_30/" + "D4B500T15_lora_send_" + str(
            i)+".log", "r"), open("rock/rock_30/" + "D4B500T15_lora_recv_" + str(i)+".log", "r"))

        _t = sum(_t) / len(_t)
        _l = sum(_l) / len(_l)
        _p = sum(_p) / len(_p)
        _r = sum(_r) / len(_r)
        _s = sum(_s) / len(_s)
        t.append(_t)
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)

    df = {"throughput (kbps)": t, "latency (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 30, "depth (cm)": 20, "moisture (ml)": 0, "soil type": "gravel", "tx_power (dBm)": 15, "datarate": 4}
    df_lora = df_lora.append(df, ignore_index=True)
    
    # Rock 40cm
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(1):

        _t, _l, _p, _r, _s = cal_10s_metric(open("rock/rock_40/" + "D4B500T15_lora_send_" + str(
            i)+".log", "r"), open("rock/rock_40/" + "D4B500T15_lora_recv_" + str(i)+".log", "r"))

        _t = sum(_t) / len(_t)
        _l = sum(_l) / len(_l)
        _p = sum(_p) / len(_p)
        _r = sum(_r) / len(_r)
        _s = sum(_s) / len(_s)
        t.append(_t)
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)

    df = {"throughput (kbps)": t, "latency (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 40, "depth (cm)": 20, "moisture (ml)": 0, "soil type": "gravel", "tx_power (dBm)": 15, "datarate": 4}
    df_lora = df_lora.append(df, ignore_index=True)
    
    
    print(df_lora)
    df_lora.to_csv(dataFolder + "avg_data_lora.csv")

def extract_avg_from_wifi():
    
    # Wifi
    
    df_wifi = {"throughput (kbps)": [], "rtt (ms)": [],
               "packetlossrate (%)": [], "snr (dB)": [], "rssi (dBm)": [], "distance (cm)": [], "depth (cm)": [], "moisture (ml)": [],"soil type": [], "tx_power (dBm)": []}
    df_wifi = pd.DataFrame(data=df_wifi)
    
    # Distance
    
    # 10cm
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(12):
        
        _t, _l, _p, _r, _s = parse_log_from_file("results/D10_B20_S1_M29/wifi_send_" + str(i) + ".log")
        t.append(sum(_t) / len(_t))
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)
    
    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)
    df = {"throughput (kbps)": t, "rtt (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 10, "depth (cm)": 20, "moisture (ml)": 0, "soil type": "yellow soil", "tx_power (dBm)": 20}
    df_wifi = df_wifi.append(df, ignore_index=True)
    
    # 20cm
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(12):

        _t, _l, _p, _r, _s = parse_log_from_file(
            "results/D20_B20_S1_M29/wifi_send_" + str(i) + ".log")
        t.append(sum(_t) / len(_t))
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)
    df = {"throughput (kbps)": t, "rtt (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 20, "depth (cm)": 20, "moisture (ml)": 0, "soil type": "yellow soil",  "tx_power (dBm)": 20}
    df_wifi = df_wifi.append(df, ignore_index=True)
    
    # 40cm
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(12):

        _t, _l, _p, _r, _s = parse_log_from_file(
            "results/D40_B20_S1_M29/wifi_send_" + str(i) + ".log")
        t.append(sum(_t) / len(_t))
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)
    df = {"throughput (kbps)": t, "rtt (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 40, "depth (cm)": 20, "moisture (ml)": 0, "soil type": "yellow soil",  "tx_power (dBm)": 20}
    df_wifi = df_wifi.append(df, ignore_index=True)
    
    # 80cm
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(12):

        _t, _l, _p, _r, _s = parse_log_from_file(
            "results/D80_B20_S1_M29/wifi_send_" + str(i) + ".log")
        t.append(sum(_t) / len(_t))
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)
    df = {"throughput (kbps)": t, "rtt (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 80, "depth (cm)": 20, "moisture (ml)": 0, "soil type": "yellow soil",  "tx_power (dBm)": 20}
    df_wifi = df_wifi.append(df, ignore_index=True)
    
    # 160cm
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(12):

        _t, _l, _p, _r, _s = parse_log_from_file(
            "results/D160_B20_S1_M29/wifi_send_" + str(i) + ".log")
        t.append(sum(_t) / len(_t))
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)
    df = {"throughput (kbps)": t, "rtt (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 160, "depth (cm)": 20, "moisture (ml)": 0, "soil type": "yellow soil", "tx_power (dBm)": 20}
    df_wifi = df_wifi.append(df, ignore_index=True)
    
    # Moisture
    
    # 0 ml
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(6):

        _t, _l, _p, _r, _s = parse_log_from_file(
            "fishtank_20cm_dry_sand_M31_6pm/T20_wifi_send_" + str(i) + ".log")
        t.append(sum(_t) / len(_t))
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)
    df = {"throughput (kbps)": t, "rtt (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 20, "depth (cm)": 20, "moisture (ml)": 0, "soil type": "sand", "tx_power (dBm)": 20}
    df_wifi = df_wifi.append(df, ignore_index=True)
    
    # 300 ml
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(3):

        _t, _l, _p, _r, _s = parse_log_from_file(
            "fishtank_20cm_dry_sand_M31_6pm/T20_wifi_send_" + str(i) + ".log")
        t.append(sum(_t) / len(_t))
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)
    df = {"throughput (kbps)": t, "rtt (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 20, "depth (cm)": 20, "moisture (ml)": 300, "soil type": "sand",  "tx_power (dBm)": 20}
    df_wifi = df_wifi.append(df, ignore_index=True)
    
    # 600 ml
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(3):

        _t, _l, _p, _r, _s = parse_log_from_file(
            "fishtank_20cm_dry_sand_M31_6pm/T20_wifi_send_" + str(i) + ".log")
        t.append(sum(_t) / len(_t))
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)
    df = {"throughput (kbps)": t, "rtt (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 20, "depth (cm)": 20, "moisture (ml)": 600, "soil type": "sand", "tx_power (dBm)": 20}
    df_wifi = df_wifi.append(df, ignore_index=True)
    
    # 1200 ml
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(3):

        _t, _l, _p, _r, _s = parse_log_from_file(
            "fishtank_20cm_dry_sand_M31_6pm/T20_wifi_send_" + str(i) + ".log")
        t.append(sum(_t) / len(_t))
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)
    df = {"throughput (kbps)": t, "rtt (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 20, "depth (cm)": 20, "moisture (ml)": 1200, "soil type": "sand", "tx_power (dBm)": 20}
    df_wifi = df_wifi.append(df, ignore_index=True)
    
    # 2400 ml
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(3):

        _t, _l, _p, _r, _s = parse_log_from_file(
            "fishtank_20cm_dry_sand_M31_6pm/T20_wifi_send_" + str(i) + ".log")
        t.append(sum(_t) / len(_t))
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)
    df = {"throughput (kbps)": t, "rtt (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 20, "depth (cm)": 20, "moisture (ml)": 2400, "soil type": "sand", "tx_power (dBm)": 20}
    df_wifi = df_wifi.append(df, ignore_index=True)
    
    # Depth rock
    
    # 20 cm
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(1):

        _t, _l, _p, _r, _s = parse_log_from_file(
            "rock/rock_20/T20_wifi_send_" + str(i) + ".log")
        t.append(sum(_t) / len(_t))
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)
    df = {"throughput (kbps)": t, "rtt (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 20, "depth (cm)": 20, "moisture (ml)": 0, "soil type": "gravel", "tx_power (dBm)": 20}
    df_wifi = df_wifi.append(df, ignore_index=True)
    
    # 30 cm
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(1):

        _t, _l, _p, _r, _s = parse_log_from_file(
            "rock/rock_30/T20_wifi_send_" + str(i) + ".log")
        t.append(sum(_t) / len(_t))
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)
    df = {"throughput (kbps)": t, "rtt (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 20, "depth (cm)": 30, "moisture (ml)": 0, "soil type": "gravel", "tx_power (dBm)": 20}
    df_wifi = df_wifi.append(df, ignore_index=True)
    
    # 40 cm
    t = []
    l = []
    p = []
    r = []
    s = []
    for i in range(1):

        _t, _l, _p, _r, _s = parse_log_from_file(
            "rock/rock_40/T20_wifi_send_" + str(i) + ".log")
        t.append(sum(_t) / len(_t))
        l.append(_l)
        p.append(_p)
        r.append(_r)
        s.append(_s)

    t = sum(t) / len(t)
    l = sum(l) / len(l)
    p = sum(p) / len(p)
    r = sum(r) / len(r)
    s = sum(s) / len(s)
    df = {"throughput (kbps)": t, "rtt (ms)": l,
          "packetlossrate (%)": p, "snr (dB)": s, "rssi (dBm)": r, "distance (cm)": 20, "depth (cm)": 40, "moisture (ml)": 0, "soil type": "gravel", "tx_power (dBm)": 20}
    df_wifi = df_wifi.append(df, ignore_index=True)


    print(df_wifi)
    df_wifi.to_csv(dataFolder+"avg_data_wifi.csv")

if __name__ == "__main__":

    extract_avg_from_lora()
    
    extract_avg_from_wifi()
    
    
    

    
    
    
    # Wifi
    
    
    