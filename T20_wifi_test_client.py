import os
import subprocess
import re
import datetime
import argparse
import time

def get_wifi_signal_strength(interface='wlan1'):
    """
    Returns the Wi-Fi signal strength (RSSI) in dBm.
    """
    cmd = ['/usr/sbin/iwlist', interface, 'scan']
    # cmd = "iwlist " + interface + " scan | grep -e Pi_adhoc -e level"
    output = subprocess.check_output(cmd).decode('utf-8')
    # output = os.system(cmd)
    # print(output)
    # Search for the line with the signal strength
    match = re.search(r'Signal level=(-\d+) dBm', output)
    if match:
        signal_strength = int(match.group(1))
        return signal_strength

    return None

# def get_wifi_signal_strength(interface='wlan1'):
    
#     wifi= pywifi.PyWiFi()
    
#     iface = wifi.interfaces()[0]
    
#     # iface.enable()
#     iface.scan()
#     time.sleep(1)
#     wifi_list = iface.scan_results()
#     rssi = 0.0
#     print(wifi_list)
    
#     for w in wifi_list:
#         print(w.rssi)
#         if (w.ssid == "Pi_adhoc"):
#             rssi = w.rssi
            
#     return rssi

def get_wifi_snr(interface='wlan1'):
    """
    Returns the Wi-Fi signal-to-noise ratio (SNR) in dB.
    """
    cmd = ['/usr/sbin/iwconfig', interface]
    output = subprocess.check_output(cmd).decode('utf-8')
    # cmd = "iwconfig " + interface
    # output = os.system(cmd)
    # Search for the line with the signal level and noise level
    match = re.search(r'Link Quality=(\d+)/(\d+)\s+Signal level=(-\d+) dBm.*Noise level=(-\d+) dBm', output)
    if match:
        signal_level = int(match.group(3))
        noise_level = int(match.group(4))
        snr = signal_level - noise_level
        return snr

    return None

# def get_wifi_snr(interface='wlan1'):
    
#     wifi= pywifi.PyWiFi()
    
#     iface = wifi.interfaces()[0]
    
#     # iface.enable()
#     iface.scan()
#     time.sleep(1)
#     wifi_list = iface.scan_results()
#     snr = 0.0
    
#     for w in wifi_list:
#         print(w.signal)
#         if (w.ssid == "Pi_adhoc"):
#             snr = w.signal
            
#     return snr

if __name__ == '__main__':
    
    # Args parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--expNumber", type=int, default=0)
    args = parser.parse_args()
    
    # Parameter
    server_ip = "192.168.1.6"
    client_ip = "192.168.1.5"
    test_runs = 1
    tx_power = 30
    iperf_time = 10
    iperf_bandwidth = 1 # Mb
    ping_time = 10
    packet_size = 100
    
    # Get current time
    now = datetime.datetime.now()
    s = datetime.datetime.strftime(now,'%Y-%m-%d-%H:%M:%S')
    
    output_folder = "/home/rpi/smartagr/wifi_log/"
    output_file = open(output_folder + "T20_wifi_send" + "_" + str(args.expNumber) + ".log", "w")
    
    
    throughput = []
    delay = []
    loss_rate = []
    
    # Set TX power
    os.system("sudo iwconfig wlan1 txpower " + str(20) )
    
    
    for i in range(test_runs):
        
        # Throughput
        result = subprocess.run(["iperf", "-B", client_ip,  "-c", server_ip, "-t", str(iperf_time), "-u", "-b", str(iperf_bandwidth) + "M", "-l", str(packet_size) + "B", "-i", str(1)], stdout=subprocess.PIPE)
        print("Round {}\n".format(str(i)))
        s = result.stdout.decode("utf-8")
        print(s)
        output_file.write(s)
        output_file.write("\n")
        
        # Latency, Packet loss rate
        result = subprocess.run(["ping", "-w", str(ping_time), "-i", "0.2",server_ip],  stdout=subprocess.PIPE)
        print("Round {}\n".format(str(i)))
        s = result.stdout.decode("utf-8")
        print(s)
        output_file.write(s)
        output_file.write("\n")
        
        # RSSI, SNR
        signal_strength = get_wifi_signal_strength()
        # signal_quality = get_wifi_signal_quality()
        snr = get_wifi_snr()
        s = f"Signal strength: {signal_strength} dBm" + "\n" + f"SNR: {snr} dB"
        print(f"Signal strength: {signal_strength} dBm")
        # print(f"Signal quality: {signal_quality}/70")
        print(f"SNR: {snr} dB")
        output_file.write(s)
        
        
        # Parser
        # print(s[-80:])
        
    
    output_file.close()
    
   

# \[[\s]*?(.+?)\][\s]*?(.+?)[\s]*?sec[\s]*?(.+?)Mbytes[\s]*?(.+?)[\s]*?Kbits/sec[\s]*?(.+?)[\s]ms*?(\d+)/[\s]*?(\d+)[\s]*?\((.+?)\)

# [3]0.0000-11.1937sec1.25MBytes939Kbits/sec20.127ms0/895(0%)

# \[(\d+)\](.+?)\-(.+?)sec(.+?)MBytes(.+?)Kbits/sec(.+?)ms(.+?)/(.+?)((.+?)\%)