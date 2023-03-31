import os
import subprocess

if __name__ == '__main__':
    
    server_ip = "192.168.1.6"
    client_ip = "192.168.1.5"
    
    # Set TX power
    os.system("sudo iwconfig wlan1 txpower " + str(1))
    subprocess.run(["iperf", "-s", "-u", "-t", "11"])


    
    
    