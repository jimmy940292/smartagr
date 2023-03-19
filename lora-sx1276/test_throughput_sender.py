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

import sys 
from time import sleep
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
        
    def send_packet(self, packet):
        self.set_mode(MODE.STDBY)
        print("Send: {}".format(packet))
        data = [int(hex(ord(c)), 0) for c in packet]
        
        data = list([0x00]*255)
        self.write_payload(data)
        self.set_mode(MODE.TX)

    def on_rx_done(self):
        # BOARD.led_on()
        print("\nRxDone")
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        data = ''.join([chr(c) for c in payload])
        print("Packet: {}".format(data))
        print("RSSI: {}".format(self.get_rssi_value()))
        print("SNR: {}".format(self.get_pkt_snr_value()))
        print()
        
        
        self.end()
                
        # Change to TX
        # BOARD.led_off()
        # self.set_dio_mapping([1,0,0,0,0,0])    # TX
        # self.set_mode(MODE.STDBY)
        # sleep(5)
        # self.clear_irq_flags(TxDone=1)
        # data = "ABCD"
        # self.send_packet(data)

    def on_tx_done(self):
        # global args
        print("\nTxDone")
        # Change to RX
        self.set_dio_mapping([0,0,0,0,0,0])    # RX
        sleep(0.01)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        self.clear_irq_flags(RxDone=1)
        
        

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
        data = "ABCD"
        self.send_packet(data)
        while True:
            sleep(0.01)
    def end(self):
        sys.stdout.flush()
        self.set_mode(MODE.SLEEP)
        print("Receive ACK")
        BOARD.teardown()
        exit()
        


if __name__ == "__main__":
    

    lora = LoRaBeacon(verbose=False)
    args = parser.parse_args(lora)

    # Setting
    lora.set_pa_config(pa_select=1)
    #lora.set_rx_crc(True)
    #lora.set_agc_auto_on(True)
    #lora.set_lna_gain(GAIN.NOT_USED)
    #lora.set_coding_rate(CODING_RATE.CR4_6)
    #lora.set_implicit_header_mode(False)
    #lora.set_pa_config(max_power=0x04, output_power=0x0F)
    #lora.set_pa_config(max_power=0x04, output_power=0b01000000)
    #lora.set_low_data_rate_optim(True)
    #lora.set_pa_ramp(PA_RAMP.RAMP_50_us)
    
    # Start
    lora.start()


# print(lora)
# #assert(lora.get_lna()['lna_gain'] == GAIN.NOT_USED)
# assert(lora.get_agc_auto_on() == 1)

# print("Beacon config:")
# print("  Wait %f s" % args.wait)
# print("  Single tx = %s" % args.single)
# print("")
# try: input("Press enter to start...")
# except: pass

# try:
#     lora.start()
# except KeyboardInterrupt:
#     sys.stdout.flush()
#     # print("")
#     sys.stderr.write("KeyboardInterrupt\n")
# finally:
#     sys.stdout.flush()
#     # print("")
#     lora.set_mode(MODE.SLEEP)
#     # print(lora)
#     BOARD.teardown()
