#!/data/data/com.termux/files/usr/bin/bash

addr=$1
port=$2
user=$3

sed -i -e "s/\(HYUNDAI_MAX_STEER =\).*/\1$1/" \
  -e "s/\(HYUNDAI_MAX_RT_DELTA =\).*/\1$2/" \
  -e "s/\(HYUNDAI_MAX_RATE_UP =\).*/\1$3/" \
  /data/openpilot/panda/board/safety/safety_hyundai.h
