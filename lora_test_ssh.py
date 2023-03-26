import sys
import os
import time
import subprocess
import argparse


# Sender
senderIP = "192.168.0.80"
senderHostName = "rpi"
senderPassword = "rpi"

# Receiver
receiverIP = "192.168.0.108"
receiverHostName = "rpiplus"
receiverPassword = "rpi"

# Lora

# Folder path
folderPath = "smartagr/lora-sx1276/"

# Log folder path
logFolderPath = "smartagr/lora-sx1276/log/"

# Current log folder path
currentLogPath = "log/"


def test_wifi(exp_number):
    
    for i in range(exp_number):
        # WiFi

        # Server command
        serverCommand = "ssh -t " + receiverHostName + \
            "@" + receiverIP + " " + "\" iperf -s -u \""
        os.system(serverCommand + "&")

        # Client command
        clientCommand = "ssh -t " + senderHostName + "@" + senderIP + \
            " " + "\" python3 smartagr/wifi_test_client.py  --expNumber " + str(exp_number) + "\""
        os.system(clientCommand)

        # Wait for test
        time.sleep(10)

    # Copy log
        clientCommand = "scp " + senderHostName + "@" + senderIP + \
            ":/home/rpi/smartagr/wifi_log/*.log " + " log/"
        os.system(clientCommand)
        
def test_lora(exp_number):
    
    for i in range(exp_number + 1):
        # Execute command
        receiverCommand = "ssh -t " + receiverHostName + "@" + receiverIP + \
            " " + "\" python3 smartagr/lora-sx1276/test_throughput_receiver.py --expNumber " + \
            str(i) + " \""
        os.system(receiverCommand + " &")
        # os.system("exit")

        senderCommand = "ssh -t " + senderHostName + "@" + senderIP + " " + \
            "\" python3 smartagr/lora-sx1276/test_throughput_sender.py --expNumber " + \
            str(i) + " \""
        os.system(senderCommand)
        # os.system("exit")

        # Wait for the receiver
        time.sleep(11)
        
    # Copy log file commmand
    receiverCommand = "scp " + receiverHostName + "@" + receiverIP + \
        ":/home/rpiplus/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(receiverCommand)

    senderCommand = "scp " + senderHostName + "@" + senderIP + \
        ":/home/rpi/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(senderCommand)

if __name__ == "__main__":
    
    # Args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--expNumber", type=int, default=0)
    args = parser.parse_args()
    
    exp_number = args.expNumber
    
    
    # Lora
    test_lora(exp_number)
    
    # WiFi
    test_wifi(exp_number)
    
    # # Run log parser
    # print()
    # parsercommand = "python3 log_parser.py "  + "--expNumber " + str(exp_number)
    # os.system(parsercommand)
