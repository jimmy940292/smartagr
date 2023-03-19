

numberofSend=10000

for i in $(seq 1 $numberofSend)
do
    # echo "$i"
    START_TIME=$SECONDS
    sudo  python3 test_throughput_sender.py
    ELAPSED_TIME=$(($SECONDS - $START_TIME))
    echo "Running time: $ELAPSED_TIME s"
    # sleep 0.001
done