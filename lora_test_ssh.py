import sys
import os
import time
import subprocess

if __name__ == "__main__":
    
    
    # Sender
    senderIP = "192.168.0.80"
    senderHostName = "rpi"
    senderPassword = "rpi"
    
    # Receiver
    receiverIP = "192.168.0.108"
    receiverHostName = "rpiplus"
    receiverPassword = "rpi"
    
    # Folder path
    folderPath = "smartagr/lora-sx1276/"
    
    # Log folder path
    logFolderPath = "smartagr/lora-sx1276/log/"
    
    # Current log folder path
    currentLogPath = "log/"
    
    # Execute command
    receiverCommand = "ssh -t " + receiverHostName + "@" + receiverIP + " " + "\" python3 smartagr/lora-sx1276/test_throughput_receiver.py \""
    os.system(receiverCommand + " &")
    # os.system("exit")
    
    senderCommand = "ssh -t " + senderHostName + "@" + senderIP + " " + "\" python3 smartagr/lora-sx1276/test_throughput_sender.py \""
    os.system(senderCommand)
    # os.system("exit")
    

    # Wait for the receiver
    time.sleep(40)

    # Copy log file commmand
    receiverCommand = "scp " + receiverHostName + "@" + receiverIP + ":/home/rpiplus/smartagr/lora-sx1276/log/receiver.log" + " log/"
    os.system(receiverCommand)
    
    senderCommand = "scp " + senderHostName + "@" + senderIP + ":/home/rpi/smartagr/lora-sx1276/log/sender.log" + " log/"
    os.system(senderCommand)

    # Run log parser
    print()
    parsercommand = "python3 log_parser.py"
    os.system(parsercommand)
    
    