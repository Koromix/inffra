#!/bin/sh -e

sudo apt install -y python3-pydbus wget

rm -rf /tmp/rezolved
mkdir /tmp/rezolved
cd /tmp/rezolved

curl -sL -o rezolved.py https://framagit.org/interhop/mla/-/raw/main/tools/rezolved/rezolved.py
curl -sL -o rezolved.service https://framagit.org/interhop/mla/-/raw/main/tools/rezolved/rezolved.service
curl -sL -o rezolved.timer https://framagit.org/interhop/mla/-/raw/main/tools/rezolved/rezolved.timer

sudo install -m0755 rezolved.py /usr/bin/rezolved
sudo install -m0644 rezolved.service /usr/lib/systemd/system/rezolved.service
sudo install -m0644 rezolved.timer /usr/lib/systemd/system/rezolved.timer

sudo systemctl daemon-reload
sudo systemctl enable rezolved.timer
sudo systemctl start rezolved.timer
