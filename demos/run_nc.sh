#!/bin/sh

nc -lk 2222 0</tmp/backpipe | nc 127.0.0.1 2200 | tee /tmp/backpipe
