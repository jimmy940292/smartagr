

sudo ifconfig wlan1 down
sudo iwconfig wlan1 mode ad-hoc 
sudo iwconfig wlan1 essid Pi_adhoc 
sudo iwconfig wlan1 channel 1
sudo ifconfig wlan1 up
sudo ifconfig wlan1 192.168.1.6