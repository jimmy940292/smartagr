# smartagr

## Wi-Fi
Test the  wifi transmission between two RPIs

### Set wifi interface to the ad hoc mode

    sh wifi_setting_1.sh # Sender (rpi)
    sh wifi_setting_2.sh # Receiver (rpiplus)

### Receiver

    python wifi_test_server.py
  
### Sender

    python wifi_test_client.py

## LoRa
Test the  wifi transmission between two RPIs

lora module from https://github.com/raspberrypi-tw/lora-sx1276

    cd lora-sx1276/02-p2p

### Receiver

    sudo python test_throughput_receiver.py
  
### Sender

    sudo python test_throughput_sender.py
