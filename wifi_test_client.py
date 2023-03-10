import os
import subprocess

if __name__ == '__main__':
    
    server_ip = "192.168.1.6"
    client_ip = "192.168.1.5"
    
    output_file = open("wifi_test_client.log", "w")
    
    
    
    
    throughput = []
    delay = []
    loss_rate = []
    
    
    for i in range(1):
        result = subprocess.run(["iperf", "-B", client_ip,  "-c", server_ip, "-t", "10", "-u", "-b", "1M"], stdout=subprocess.PIPE)
        print("Round {}\n".format(str(i)))
        
        s = result.stdout.decode("utf-8")
        print(s)
        output_file.write(s)
        
        # print(s[-80:])
        
    output_file.close()

# \[[\s]*?(.+?)\][\s]*?(.+?)[\s]*?sec[\s]*?(.+?)Mbytes[\s]*?(.+?)[\s]*?Kbits/sec[\s]*?(.+?)[\s]ms*?(\d+)/[\s]*?(\d+)[\s]*?\((.+?)\)

# [3]0.0000-11.1937sec1.25MBytes939Kbits/sec20.127ms0/895(0%)

# \[(\d+)\](.+?)\-(.+?)sec(.+?)MBytes(.+?)Kbits/sec(.+?)ms(.+?)/(.+?)((.+?)\%)