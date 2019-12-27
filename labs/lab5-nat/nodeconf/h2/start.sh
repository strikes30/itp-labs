#!/bin/sh

BASE_DIR=/home/user/mytests/ospf3routers/nodeconf
NODE_NAME=h2
IP_ADDR=192.168.0.2/24
GW_ADDR=192.168.0.1

ip addr add $IP_ADDR dev $NODE_NAME-eth0 
ip route add default via $GW_ADDR dev $NODE_NAME-eth0
