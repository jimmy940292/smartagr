import sys
import os


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
    receiverCommand = ""
    
    senderCommand = ""
    
    # Copy log file commmand
    
    