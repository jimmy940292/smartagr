import sys
import os
import time


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
    receiverCommand = "ssh " + receiverHostName + "@" + receiverIP + " " + "\" cd smartagr/lora-sx1276/ | python3 test_throughput_receiver.py \""
    os.system(receiverCommand)
    
    senderCommand = "ssh " + senderHostName + "@" + senderIP + " " + "\" cd smartagr/lora-sx1276/ | python3 test_throughput_sender.py \""
    os.system(senderCommand)
    
    
    time.sleep(30)
    # Copy log file commmand
    receiverCommand = "scp " + receiverHostName + "@" + receiverIP + ":/home/rpiplus/smartagr/lora-sx1276/log/receiver.log" + " log/"
    os.system(receiverCommand)
    
    senderCommand = "scp " + senderHostName + "@" + senderIP + ":/home/rpi/smartagr/lora-sx1276/log/sender.log" + " log/"
    os.system(senderCommand)
    
    