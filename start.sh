#!/bin/bash
python3 server.py &
sleep 3
python3 auto.py &
wait
