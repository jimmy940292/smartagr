#!/usr/bin/env python3

""" A simple continuous receiver class. """

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
# python p2p_recv.py -f 433 -b BW125 -s 12

# Python Module
import sys
import socket
import struct 
import time
from datetime import datetime
import argparse
import os

# Lora Module
sys.path.insert(0, '../')        
from SX127x.LoRa import *
from SX127x.LoRaArgumentParser import LoRaArgumentParser
from SX127x.board_config import BOARD

BOARD.setup()

parser = LoRaArgumentParser("Continous LoRa receiver.")


class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        
        # Variable
        self.logfile = None
        self.testTime = 10
        self.startTime = None
        
    def read_packet_payload(self, data):
        
        seq_data = []
        for c in data:
            if(chr(c) == 'a'):
                break
            else:
                seq_data.append(chr(c))
                
        return ''.join(seq_data)

    def send_packet(self, packet):
        # self.set_mode(MODE.STDBY)
        # print("Send: {}".format(packet))
        data = [int(hex(ord(c)), 0) for c in packet]
        self.write_payload(data)
        self.set_mode(MODE.TX)
        
        
        
    def on_rx_done(self):
        
        receiveTime = time.time()
        # print("\nRxDone")
        self.clear_irq_flags(RxDone=1)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        payload = self.read_payload(nocheck=True)
        
        # Read payload
        data = self.read_packet_payload(payload)
        # print("Packet: {}".format(data))
        # print("RSSI: {}".format(self.get_rssi_value()))
        # print("SNR: {}".format(self.get_pkt_snr_value()))
        
        # Write
        rssi = self.get_rssi_value()
        snr = self.get_pkt_snr_value()
        self.logfile.write(str(data) + "," + str(len(payload)) + "," + str(receiveTime) + "," + str(rssi) + "," + str(snr) + "\n")
        
        

    def on_tx_done(self):
        print("\nTxDone")
        # # print(self.get_irq_flags())
        

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
        
    def end(self):
        print("Receive End\n")
        self.logfile.close()
        sys.stdout.flush()
        self.set_mode(MODE.SLEEP)
        BOARD.teardown()
        exit()

    def start(self):
        global args
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        
        self.logfile = open( args.logFilePath + args.logFileName + "_" + str(args.expNumber) + ".log", "w")
        self.startTime = datetime.now()
        
        while True:
            # sleep(0.01)
            s = (datetime.now() - self.startTime).total_seconds()
            if( s > self.testTime):
                self.end()
            else:
                time.sleep(0.01)
            # rssi_value = self.get_rssi_value()
            # status = self.get_modem_status()
            # sys.stdout.flush()
            
            # sys.stdout.write("\r%d %d %d" % (rssi_value, status['rx_ongoing'], status['modem_clear']))

if __name__ == "__main__":
    
    # Args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--txpower", type=float, default=15)
    parser.add_argument("--logFileName", type=str, default="D2B125T1_lora_recv")
    parser.add_argument("--logFilePath", type=str, default="/home/rpiplus/smartagr/lora-sx1276/log/")
    parser.add_argument("--expNumber", type=int, default=0)
    args = parser.parse_args()
    
    
    lora = LoRaRcvCont(verbose=False)
    # args = parser.parse_args(lora)

    # Setting
    lora.set_mode(MODE.STDBY)
    lora.set_pa_config(pa_select=1)
    lora.set_pa_dac(True)
    #lora.set_rx_crc(True)
    
    # DR1
    # lora.set_coding_rate(CODING_RATE.CR4_5)
    # lora.set_bw(BW.BW125)
    
    # # DR2
    lora.set_coding_rate(CODING_RATE.CR4_6)
    lora.set_bw(BW.BW125)
    
    # DR4
    # lora.set_coding_rate(CODING_RATE.CR4_8)
    # lora.set_bw(BW.BW500)
    
    # lora.set_pa_config(max_power=0x0F, output_power=0x0F)
    lora.set_pa_config(max_power=1, output_power=1) 
    #lora.set_lna_gain(GAIN.G1)
    #lora.set_implicit_header_mode(False)
    lora.set_low_data_rate_optim(False)
    #lora.set_pa_ramp(PA_RAMP.RAMP_50_us)
    #lora.set_agc_auto_on(True)
    
    # Synchronize timestamp
    # ntp_client = ntplib.NTPClient()
    # # response = ntp_client.request("pool.ntp.org")
    # response = ntp_client.request("192.168.0.70")
    # ntp_timestamp = response.tx_time
    
    # local_time = time.time()
    # lora.ntpOffset = ntp_timestamp - local_time
    
    # Start
    lora.start()
    

    # print(lora)
    # assert(lora.get_agc_auto_on() == 1)

    # try: input("Press enter to start...")
    # except: pass

# try:
#     lora.start()
# except KeyboardInterrupt:
#     sys.stdout.flush()
#     print("")
#     sys.stderr.write("KeyboardInterrupt\n")
# finally:
#     sys.stdout.flush()
#     print("")
#     lora.set_mode(MODE.SLEEP)
#     print(lora)
#     BOARD.teardown()