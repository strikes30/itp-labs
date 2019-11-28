#!/bin/bash

# add GPG key
wget https://deb.frrouting.org/frr/keys.asc 
sudo apt-key add keys.asc
rm keys.asc

# possible values for FRRVER: frr-6 frr-7 frr-stable
# frr-stable will be the latest official stable release
FRRVER="frr-stable"
echo deb https://deb.frrouting.org/frr $(lsb_release -s -c) $FRRVER | sudo tee -a /etc/apt/sources.list.d/frr.list

# update and install FRR
sudo apt update && sudo apt -y install frr frr-pythontools

