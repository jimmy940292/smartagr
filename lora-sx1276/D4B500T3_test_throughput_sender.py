#!/usr/bin/env python3

""" A simple beacon transmitter class to send a 1-byte message (0x0f) in regular time intervals. """

# Copyright 2015 Mayer Analytics Ltd.
#
# This file is part of pySX127x.
#
# pySX127x is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pySX127x is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You can be released from the requirements of the license by obtaining a commercial license. Such a license is
# mandatory as soon as you develop commercial activities involving pySX127x without disclosing the source code of your
# own applications, or shipping pySX127x with a closed source product.
#
# You should have received a copy of the GNU General Public License along with pySX127.  If not, see
# <http://www.gnu.org/licenses/>.

# usage:
# python p2p_send.py -f 433 -b BW125 -s 12

# Python Module
import sys 
import socket
import struct
import time
import ntplib
import os
import argparse

# Lora Module
sys.path.insert(0, '..')        
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD

BOARD.setup()

parser = LoRaArgumentParser("A simple LoRa beacon")
parser.add_argument('--single', '-S', dest='single', default=False, action="store_true", help="Single transmission")
parser.add_argument('--wait', '-w', dest='wait', default=1, action="store", type=float, help="Waiting time between transmissions (default is 0s)")


class LoRaBeacon(LoRa):

    tx_counter = 0

    def __init__(self, verbose=False):
        super(LoRaBeacon, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([1,0,0,0,0,0])
        
        # Variable
        self.sentPacket = 0
        self.AvgThroughput = 0.0
        self.throughputList = None
        self.sendTime = None
        self.receiveTime = None
        self.packetSize = 100
        self.intervalTime = 0.00 # s
        self.sequenceNumber = 0
        self.logfile = None
        self.logFileName = ""
        self.logFilePath = ""
        self.numberofPackets = 100
        self.ntpOffset = None
        self.txpower = 0.0
        self.expNumber = 0
        self.data = []
        
        
    def set_packet_payload(self, seq):
        # data = [int(hex(ord(c)), 0) for c in seq]
        
        # remain_size = self.packetSize - len(data)
        
        # for i in range(remain_size):
        #     data.append(int(hex(ord('a')), 0))
        
        seq_data = [int(hex(ord(c)), 0) for c in seq]
        self.data[:len(seq_data)] = seq_data
        
        # return data
        
    def send_packet(self, seq):
        # print("Send: {}".format(packet))
        
        
        self.set_packet_payload(seq)
        
        
        # # Add length
        # if(len(data) < self.packetsSize):
        #     orginSize = len(data)
        #     for i in range(self.packetSize - originSize):
        #         data.append([])
        
        # data = list([0x00]*self.packetSize)
        # print(len(self.data))
        self.write_payload(self.data)
        self.set_mode(MODE.TX)
        
        # Write
        self.sendTime = time.time()
        self.logfile.write(str(self.sequenceNumber) + "," + str(len(self.data)) + "," + str(self.sendTime) + "\n")
        self.sentPacket +=1
        self.sequenceNumber +=1
        
        

    def on_rx_done(self):
        
        print("\nRxDone")
        
        # # Calculate throughput
        # self.receiveTime = time.time() 
        
        # self.throughputList[self.sentPacket -1] = self.packetSize / (self.receiveTime - self.sendTime)
        
        # # payload = self.read_payload(nocheck=True)
        # # data = ''.join([chr(c) for c in payload])
        # # print("Packet: {}".format(data))
        # # print("RSSI: {}".format(self.get_rssi_value()))
        # # print("SNR: {}".format(self.get_pkt_snr_value()))
        # # print()
        # # self.end()
                

    def on_tx_done(self):
        # global args
        # print("\nTxDone")
        # self.set_mode(MODE.STDBY)
        
        # time.sleep(self.intervalTime)
        self.clear_irq_flags(TxDone=1)
        if (self.sentPacket < self.numberofPackets):
            self.send_packet(str(self.sequenceNumber))
        else:
            self.end()

            
        
    
    def on_cad_done(self):
        print("\non_CadDone")
        print(self.get_irq_flags())

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())

    def on_valid_header(self):
        print("\non_ValidHeader")
        print(self.get_irq_flags())

    def on_payload_crc_error(self):
        print("\non_PayloadCrcError")
        print(self.get_irq_flags())

    def on_fhss_change_channel(self):
        print("\non_FhssChangeChannel")
        print(self.get_irq_flags())

    def start(self):
        global args
        self.tx_counter = 0
        # BOARD.led_on()
        # self.write_payload([0x0f])
        data = str(self.sequenceNumber)


        self.logfile = open(self.logFilePath + self.logFileName + "_" + str(self.expNumber) + ".log", "w")
        
        self.throughputList = [0.0] * self.numberofPackets 
        
        self.send_packet(data)
        while(1):
            time.sleep(0.01)
            continue
            # if(self.sentPacket > self.numberofPackets):
                
            #     # Calculate Average throughput
            #     # self.AvgThroughput = sum(self.throughputList) / len(self.throughputList)
            #     # print("Avg throughput: {} kbps".format(self.AvgThroughput / 1000))
                
            #     self.end()
    def end(self):
        
        # Close log file
        self.logfile.close()
        
        sys.stdout.flush()
        self.set_mode(MODE.SLEEP)
        # print("Receive ACK")
        BOARD.teardown()
        exit()
        

def test_syn_timestamp():
    
    while(1):
        print("Timestamp: {}".format(round(time.time(), 1)))
        time.sleep(1)
        
       
        


if __name__ == "__main__":
    
    
    # Test syn timestamp
    # test_syn_timestamp()
    
    # Args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--txpower", type=float, default=15)
    parser.add_argument("--logFileName", type=str, default="D4B500T3_lora_send")
    parser.add_argument("--logFilePath", type=str, default="/home/rpi/smartagr/lora-sx1276/log/")
    parser.add_argument("--expNumber", type=int, default=0)
    args = parser.parse_args()
    
    lora = LoRaBeacon(verbose=False)
    # args = parser.parse_args(lora)
    
    # Set args
    lora.txpower = args.txpower
    lora.logFileName = args.logFileName
    lora.logFilePath = args.logFilePath
    lora.expNumber = args.expNumber 
    

    # Setting
    lora.set_mode(MODE.STDBY)
    lora.set_pa_config(pa_select=1)
    lora.set_pa_dac(True)
    #lora.set_rx_crc(True)
    # lora.set_agc_auto_on(True)
    #lora.set_lna_gain(GAIN.NOT_USED)
    
    # DR1
    # lora.set_coding_rate(CODING_RATE.CR4_5)
    # lora.set_bw(BW.BW125)
    
    # # DR2
    # lora.set_coding_rate(CODING_RATE.CR4_6)
    # lora.set_bw(BW.BW125)
    
    # # DR4
    lora.set_coding_rate(CODING_RATE.CR4_8)
    lora.set_bw(BW.BW500)
    
    #lora.set_implicit_header_mode(False)
    # lora.set_pa_config(max_power=0x0F, output_power=0x0F)
    lora.set_pa_config(max_power=3, output_power=3) 
    lora.set_low_data_rate_optim(False)
    #lora.set_pa_ramp(PA_RAMP.RAMP_50_us)
    
   
    
    # # Synchronize timestamp
    # ntp_client = ntplib.NTPClient()
    # # response = ntp_client.request("pool.ntp.org")
    # response = ntp_client.request("192.168.0.70")
    # ntp_timestamp = response.tx_time
    # local_time = time.time()
    # lora.ntpOffset = ntp_timestamp - local_time
    
    # Set data
    # lora.data = list([int(hex(ord('a')), 0)] * lora.packetSize)
    
    # Start
    lora.start()
    
