import sys
import os
import time
import subprocess
import argparse


# Sender
senderIP = "10.0.0.1"
senderHostName = "rpi"
senderPassword = "rpi"
senderp = "sshpass -p " + senderPassword + " "

# Receiver
receiverIP = "10.0.1.1"
receiverHostName = "rpiplus"
receiverPassword = "rpi"
receiverp = "sshpass -p " + receiverPassword + " "

# Lora

# Folder path
folderPath = "smartagr/lora-sx1276/"

# Log folder path
logFolderPath = "smartagr/lora-sx1276/log/"

# Current log folder path
currentLogPath = "log/"


def T1_test_wifi(exp_number):
    
    # Delete old log
    os.system(senderp + "ssh -t " + senderHostName + "@" + senderIP + " " + " rm /home/rpi/smartagr/wifi_log/*.log")
    
    
    
    for i in range(exp_number + 1):
        # WiFi

        # Server command
        serverCommand = "ssh -t " + receiverHostName + \
            "@" + receiverIP + " " + "\" iperf -s -u \""
        os.system(receiverp + serverCommand + "&")
        serverCommand = "ssh -t " + receiverHostName + \
            "@" + receiverIP + " " + "\" python3 smartagr/T1_wifi_test_server.py \""
        

        # Client command
        clientCommand = "ssh -t " + senderHostName + "@" + senderIP + \
            " " + "\" python3 smartagr/T1_wifi_test_client.py  --expNumber " + str(i) + "\""
        os.system(senderp + clientCommand)

        # Wait for test
        time.sleep(10)

    # Copy log
    clientCommand = "scp " + senderHostName + "@" + senderIP + \
        ":/home/rpi/smartagr/wifi_log/*.log " + " log/"
    os.system(senderp + clientCommand)
    

def T3_test_wifi(exp_number):

    # Delete old log
    os.system(senderp + "ssh -t " + senderHostName + "@" +
              senderIP + " " + " rm /home/rpi/smartagr/wifi_log/*.log")

    for i in range(exp_number + 1):
        # WiFi

        # Server command
        serverCommand = "ssh -t " + receiverHostName + \
            "@" + receiverIP + " " + "\" iperf -s -u \""
        os.system(receiverp + serverCommand + "&")
        serverCommand = "ssh -t " + receiverHostName + \
            "@" + receiverIP + " " + "\" python3 smartagr/T3_wifi_test_server.py \""

        # Client command
        clientCommand = "ssh -t " + senderHostName + "@" + senderIP + \
            " " + "\" python3 smartagr/T3_wifi_test_client.py  --expNumber " + \
            str(i) + "\""
        os.system(senderp + clientCommand)

        # Wait for test
        time.sleep(10)

    # Copy log
    clientCommand = "scp " + senderHostName + "@" + senderIP + \
        ":/home/rpi/smartagr/wifi_log/*.log " + " log/"
    os.system(senderp + clientCommand)
    

def T10_test_wifi(exp_number):

    # Delete old log
    os.system(senderp + "ssh -t " + senderHostName + "@" +
              senderIP + " " + " rm /home/rpi/smartagr/wifi_log/*.log")

    for i in range(exp_number + 1):
        # WiFi

        # Server command
        serverCommand = "ssh -t " + receiverHostName + \
            "@" + receiverIP + " " + "\" iperf -s -u \""
        os.system(receiverp + serverCommand + "&")
        serverCommand = "ssh -t " + receiverHostName + \
            "@" + receiverIP + " " + "\" python3 smartagr/T10_wifi_test_server.py \""

        # Client command
        clientCommand = "ssh -t " + senderHostName + "@" + senderIP + \
            " " + "\" python3 smartagr/T10_wifi_test_client.py  --expNumber " + \
            str(i) + "\""
        os.system(senderp + clientCommand)

        # Wait for test
        time.sleep(10)

    # Copy log
    clientCommand = "scp " + senderHostName + "@" + senderIP + \
        ":/home/rpi/smartagr/wifi_log/*.log " + " log/"
    os.system(senderp + clientCommand)
    

def T5_test_wifi(exp_number):

    # Delete old log
    os.system(senderp + "ssh -t " + senderHostName + "@" +
              senderIP + " " + " rm /home/rpi/smartagr/wifi_log/*.log")

    for i in range(exp_number + 1):
        # WiFi

        # Server command
        serverCommand = "ssh -t " + receiverHostName + \
            "@" + receiverIP + " " + "\" iperf -s -u \""
        os.system(receiverp + serverCommand + "&")
        serverCommand = "ssh -t " + receiverHostName + \
            "@" + receiverIP + " " + "\" python3 smartagr/T5_wifi_test_server.py \""

        # Client command
        clientCommand = "ssh -t " + senderHostName + "@" + senderIP + \
            " " + "\" python3 smartagr/T5_wifi_test_client.py  --expNumber " + \
            str(i) + "\""
        os.system(senderp + clientCommand)

        # Wait for test
        time.sleep(10)

    # Copy log
    clientCommand = "scp " + senderHostName + "@" + senderIP + \
        ":/home/rpi/smartagr/wifi_log/*.log " + " log/"
    os.system(senderp + clientCommand)
    

def T20_test_wifi(exp_number):

    # Delete old log
    os.system(senderp + "ssh -t " + senderHostName + "@" +
              senderIP + " " + " rm /home/rpi/smartagr/wifi_log/*.log")

    for i in range(exp_number + 1):
        # WiFi

        # Server command
        serverCommand = "ssh -t " + receiverHostName + \
            "@" + receiverIP + " " + "\" iperf -s -u \""
        os.system(receiverp + serverCommand + "&")
        serverCommand = "ssh -t " + receiverHostName + \
            "@" + receiverIP + " " + "\" python3 smartagr/T20_wifi_test_server.py \""

        # Client command
        clientCommand = "ssh -t " + senderHostName + "@" + senderIP + \
            " " + "\" python3 smartagr/T20_wifi_test_client.py  --expNumber " + \
            str(i) + "\""
        os.system(senderp + clientCommand)

        # Wait for test
        time.sleep(10)

    # Copy log
    clientCommand = "scp " + senderHostName + "@" + senderIP + \
        ":/home/rpi/smartagr/wifi_log/*.log " + " log/"
    os.system(senderp + clientCommand)
        
def D1T1_test_lora(exp_number):
    
    # Delete old log
    os.system(senderp + "ssh -t " + senderHostName + "@" + senderIP + " " + " rm /home/rpi/smartagr/lora-sx1276/log/*.log")
    os.system(receiverp + "ssh -t " + receiverHostName + "@" + receiverIP + " " + " rm /home/rpiplus/smartagr/lora-sx1276/log/*.log")
    
    for i in range(exp_number + 1):
        # Execute command
        receiverCommand = "ssh -t " + receiverHostName + "@" + receiverIP + \
            " " + "\" python3 smartagr/lora-sx1276/D1B125T1_test_throughput_receiver.py --expNumber " + \
            str(i) + " \""
        os.system(receiverp + receiverCommand + " &")
        # os.system("exit")

        senderCommand = "ssh -t " + senderHostName + "@" + senderIP + " " + \
            "\" python3 smartagr/lora-sx1276/D1B125T1_test_throughput_sender.py --expNumber " + \
            str(i) + " \""
        os.system(senderp + senderCommand)
        # os.system("exit")

        # Wait for the receiver
        time.sleep(11)
        
    # Copy log file commmand
    receiverCommand = "scp " + receiverHostName + "@" + receiverIP + \
        ":/home/rpiplus/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(receiverp + receiverCommand)

    senderCommand = "scp " + senderHostName + "@" + senderIP + \
        ":/home/rpi/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(senderp + senderCommand)
    

def D1T3_test_lora(exp_number):

    # Delete old log
    os.system(senderp + "ssh -t " + senderHostName + "@" + senderIP +
              " " + " rm /home/rpi/smartagr/lora-sx1276/log/*.log")
    os.system(receiverp + "ssh -t " + receiverHostName + "@" + receiverIP +
              " " + " rm /home/rpiplus/smartagr/lora-sx1276/log/*.log")

    for i in range(exp_number + 1):
        # Execute command
        receiverCommand = "ssh -t " + receiverHostName + "@" + receiverIP + \
            " " + "\" python3 smartagr/lora-sx1276/D1B125T3_test_throughput_receiver.py --expNumber " + \
            str(i) + " \""
        os.system(receiverp + receiverCommand + " &")
        # os.system("exit")

        senderCommand = "ssh -t " + senderHostName + "@" + senderIP + " " + \
            "\" python3 smartagr/lora-sx1276/D1B125T3_test_throughput_sender.py --expNumber " + \
            str(i) + " \""
        os.system(senderp + senderCommand)
        # os.system("exit")

        # Wait for the receiver
        time.sleep(11)

    # Copy log file commmand
    receiverCommand = "scp " + receiverHostName + "@" + receiverIP + \
        ":/home/rpiplus/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(receiverp + receiverCommand)

    senderCommand = "scp " + senderHostName + "@" + senderIP + \
        ":/home/rpi/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(senderp + senderCommand)
    

def D1T15_test_lora(exp_number):

    # Delete old log
    os.system(senderp + "ssh -t " + senderHostName + "@" + senderIP +
              " " + " rm /home/rpi/smartagr/lora-sx1276/log/*.log")
    os.system(receiverp + "ssh -t " + receiverHostName + "@" + receiverIP +
              " " + " rm /home/rpiplus/smartagr/lora-sx1276/log/*.log")

    for i in range(exp_number + 1):
        # Execute command
        receiverCommand = "ssh -t " + receiverHostName + "@" + receiverIP + \
            " " + "\" python3 smartagr/lora-sx1276/D1B125T15_test_throughput_receiver.py --expNumber " + \
            str(i) + " \""
        os.system(receiverp + receiverCommand + " &")
        # os.system("exit")

        senderCommand = "ssh -t " + senderHostName + "@" + senderIP + " " + \
            "\" python3 smartagr/lora-sx1276/D1B125T15_test_throughput_sender.py --expNumber " + \
            str(i) + " \""
        os.system(senderp + senderCommand)
        # os.system("exit")

        # Wait for the receiver
        time.sleep(11)

    # Copy log file commmand
    receiverCommand = "scp " + receiverHostName + "@" + receiverIP + \
        ":/home/rpiplus/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(receiverp + receiverCommand)

    senderCommand = "scp " + senderHostName + "@" + senderIP + \
        ":/home/rpi/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(senderp + senderCommand)
    

def D2T1_test_lora(exp_number):

    # Delete old log
    os.system(senderp + "ssh -t " + senderHostName + "@" + senderIP +
              " " + " rm /home/rpi/smartagr/lora-sx1276/log/*.log")
    os.system(receiverp + "ssh -t " + receiverHostName + "@" + receiverIP +
              " " + " rm /home/rpiplus/smartagr/lora-sx1276/log/*.log")

    for i in range(exp_number + 1):
        # Execute command
        receiverCommand = "ssh -t " + receiverHostName + "@" + receiverIP + \
            " " + "\" python3 smartagr/lora-sx1276/D2B125T1_test_throughput_receiver.py --expNumber " + \
            str(i) + " \""
        os.system(receiverp + receiverCommand + " &")
        # os.system("exit")

        senderCommand = "ssh -t " + senderHostName + "@" + senderIP + " " + \
            "\" python3 smartagr/lora-sx1276/D2B125T1_test_throughput_sender.py --expNumber " + \
            str(i) + " \""
        os.system(senderp + senderCommand)
        # os.system("exit")

        # Wait for the receiver
        time.sleep(11)

    # Copy log file commmand
    receiverCommand = "scp " + receiverHostName + "@" + receiverIP + \
        ":/home/rpiplus/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(receiverp + receiverCommand)

    senderCommand = "scp " + senderHostName + "@" + senderIP + \
        ":/home/rpi/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(senderp + senderCommand)
    

def D2T3_test_lora(exp_number):

    # Delete old log
    os.system(senderp + "ssh -t " + senderHostName + "@" + senderIP +
              " " + " rm /home/rpi/smartagr/lora-sx1276/log/*.log")
    os.system(receiverp + "ssh -t " + receiverHostName + "@" + receiverIP +
              " " + " rm /home/rpiplus/smartagr/lora-sx1276/log/*.log")

    for i in range(exp_number + 1):
        # Execute command
        receiverCommand = "ssh -t " + receiverHostName + "@" + receiverIP + \
            " " + "\" python3 smartagr/lora-sx1276/D2B125T3_test_throughput_receiver.py --expNumber " + \
            str(i) + " \""
        os.system(receiverp + receiverCommand + " &")
        # os.system("exit")

        senderCommand = "ssh -t " + senderHostName + "@" + senderIP + " " + \
            "\" python3 smartagr/lora-sx1276/D2B125T3_test_throughput_sender.py --expNumber " + \
            str(i) + " \""
        os.system(senderp + senderCommand)
        # os.system("exit")

        # Wait for the receiver
        time.sleep(11)

    # Copy log file commmand
    receiverCommand = "scp " + receiverHostName + "@" + receiverIP + \
        ":/home/rpiplus/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(receiverp + receiverCommand)

    senderCommand = "scp " + senderHostName + "@" + senderIP + \
        ":/home/rpi/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(senderp + senderCommand)
    

def D2T15_test_lora(exp_number):

    # Delete old log
    os.system(senderp + "ssh -t " + senderHostName + "@" + senderIP +
              " " + " rm /home/rpi/smartagr/lora-sx1276/log/*.log")
    os.system(receiverp + "ssh -t " + receiverHostName + "@" + receiverIP +
              " " + " rm /home/rpiplus/smartagr/lora-sx1276/log/*.log")

    for i in range(exp_number + 1):
        # Execute command
        receiverCommand = "ssh -t " + receiverHostName + "@" + receiverIP + \
            " " + "\" python3 smartagr/lora-sx1276/D2B125T15_test_throughput_receiver.py --expNumber " + \
            str(i) + " \""
        os.system(receiverp + receiverCommand + " &")
        # os.system("exit")

        senderCommand = "ssh -t " + senderHostName + "@" + senderIP + " " + \
            "\" python3 smartagr/lora-sx1276/D2B125T15_test_throughput_sender.py --expNumber " + \
            str(i) + " \""
        os.system(senderp + senderCommand)
        # os.system("exit")

        # Wait for the receiver
        time.sleep(11)

    # Copy log file commmand
    receiverCommand = "scp " + receiverHostName + "@" + receiverIP + \
        ":/home/rpiplus/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(receiverp + receiverCommand)

    senderCommand = "scp " + senderHostName + "@" + senderIP + \
        ":/home/rpi/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(senderp + senderCommand)
    

def D4T1_test_lora(exp_number):

    # Delete old log
    os.system(senderp + "ssh -t " + senderHostName + "@" + senderIP +
              " " + " rm /home/rpi/smartagr/lora-sx1276/log/*.log")
    os.system(receiverp + "ssh -t " + receiverHostName + "@" + receiverIP +
              " " + " rm /home/rpiplus/smartagr/lora-sx1276/log/*.log")

    for i in range(exp_number + 1):
        # Execute command
        receiverCommand = "ssh -t " + receiverHostName + "@" + receiverIP + \
            " " + "\" python3 smartagr/lora-sx1276/D4B500T1_test_throughput_receiver.py --expNumber " + \
            str(i) + " \""
        os.system(receiverp + receiverCommand + " &")
        # os.system("exit")

        senderCommand = "ssh -t " + senderHostName + "@" + senderIP + " " + \
            "\" python3 smartagr/lora-sx1276/D4B500T1_test_throughput_sender.py --expNumber " + \
            str(i) + " \""
        os.system(senderp + senderCommand)
        # os.system("exit")

        # Wait for the receiver
        time.sleep(11)

    # Copy log file commmand
    receiverCommand = "scp " + receiverHostName + "@" + receiverIP + \
        ":/home/rpiplus/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(receiverp + receiverCommand)

    senderCommand = "scp " + senderHostName + "@" + senderIP + \
        ":/home/rpi/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(senderp + senderCommand)


def D4T3_test_lora(exp_number):

    # Delete old log
    os.system(senderp + "ssh -t " + senderHostName + "@" + senderIP +
              " " + " rm /home/rpi/smartagr/lora-sx1276/log/*.log")
    os.system(receiverp + "ssh -t " + receiverHostName + "@" + receiverIP +
              " " + " rm /home/rpiplus/smartagr/lora-sx1276/log/*.log")

    for i in range(exp_number + 1):
        # Execute command
        receiverCommand = "ssh -t " + receiverHostName + "@" + receiverIP + \
            " " + "\" python3 smartagr/lora-sx1276/D4B500T3_test_throughput_receiver.py --expNumber " + \
            str(i) + " \""
        os.system(receiverp + receiverCommand + " &")
        # os.system("exit")

        senderCommand = "ssh -t " + senderHostName + "@" + senderIP + " " + \
            "\" python3 smartagr/lora-sx1276/D4B500T3_test_throughput_sender.py --expNumber " + \
            str(i) + " \""
        os.system(senderp + senderCommand)
        # os.system("exit")

        # Wait for the receiver
        time.sleep(11)

    # Copy log file commmand
    receiverCommand = "scp " + receiverHostName + "@" + receiverIP + \
        ":/home/rpiplus/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(receiverp + receiverCommand)

    senderCommand = "scp " + senderHostName + "@" + senderIP + \
        ":/home/rpi/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(senderp + senderCommand)
    

def D4T15_test_lora(exp_number):

    # Delete old log
    os.system(senderp + "ssh -t " + senderHostName + "@" + senderIP +
              " " + " rm /home/rpi/smartagr/lora-sx1276/log/*.log")
    os.system(receiverp + "ssh -t " + receiverHostName + "@" + receiverIP +
              " " + " rm /home/rpiplus/smartagr/lora-sx1276/log/*.log")

    for i in range(exp_number + 1):
        # Execute command
        receiverCommand = "ssh -t " + receiverHostName + "@" + receiverIP + \
            " " + "\" python3 smartagr/lora-sx1276/D4B500T15_test_throughput_receiver.py --expNumber " + \
            str(i) + " \""
        os.system(receiverp + receiverCommand + " &")
        # os.system("exit")

        senderCommand = "ssh -t " + senderHostName + "@" + senderIP + " " + \
            "\" python3 smartagr/lora-sx1276/D4B500T15_test_throughput_sender.py --expNumber " + \
            str(i) + " \""
        os.system(senderp + senderCommand)
        # os.system("exit")

        # Wait for the receiver
        time.sleep(11)

    # Copy log file commmand
    receiverCommand = "scp " + receiverHostName + "@" + receiverIP + \
        ":/home/rpiplus/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(receiverp + receiverCommand)

    senderCommand = "scp " + senderHostName + "@" + senderIP + \
        ":/home/rpi/smartagr/lora-sx1276/log/*.log" + " log/"
    os.system(senderp + senderCommand)

if __name__ == "__main__":
    
    # Args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--expNumber", type=int, default=0)
    args = parser.parse_args()
    
    exp_number = args.expNumber
    tx_power = args.txpower
    
    
    # Lora
    D1T1_test_lora(exp_number)
    D1T3_test_lora(exp_number)
    D1T15_test_lora(exp_number)
    D2T1_test_lora(exp_number)
    D2T3_test_lora(exp_number)
    D2T15_test_lora(exp_number)
    D4T1_test_lora(exp_number)
    D4T3_test_lora(exp_number)
    D4T15_test_lora(exp_number)
    
    # WiFi
    T1_test_wifi(exp_number)
    T3_test_wifi(exp_number)
    T5_test_wifi(exp_number)
    T10_test_wifi(exp_number)
    T20_test_wifi(exp_number)
    # # Run log parser
    # print()
    # parsercommand = "python3 log_parser.py "  + "--expNumber " + str(exp_number)
    # os.system(parsercommand)
