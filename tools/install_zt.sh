#!/bin/bash -e

if [[ $# -ne 2 ]]; then
    echo "Usage: install_zt.sh <network> <moon>"
    exit 1
fi

sudo apt update
sudo apt install gpg
sudo curl -s 'https://raw.githubusercontent.com/zerotier/ZeroTierOne/master/doc/contact%40zerotier.com.gpg' | gpg --import && \
    if z=$(curl -s 'https://install.zerotier.com/' | gpg); then echo "$z" | sudo bash; fi
sudo apt install zerotier-one

sudo zerotier-cli join $1
sudo zerotier-cli orbit $2 $2
sudo zerotier-cli info
