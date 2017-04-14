#!/bin/bash
for (( ; ; ))
do
    echo "Running demo_server.py"
    (nc -lk 2222 0</tmp/backpipe & echo $!>&3) 3>pid | nc 127.0.0.1 2200 > /tmp/backpipe &
    NC_PID=$(<pid)
    python demo_server.py
    kill $NC_PID
    echo "=========================================================="
    echo "            PRESS ANY KEY TO RESTART SERVER....           "
    read -n 1 -s
    echo "=========================================================="

done
