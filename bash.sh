#!/bin/bash
cd /home/ec2-user || exit
sudo amazon-linux-extras enable python3.8
yum clean metadata
sudo yum install python3.8 -y
curl -O https://bootstrap.pypa.io/get-pip.py
python3.8 get-pip.py --user
sudo yum install git -y
git clone https://github.com/sinanartun/binance_A1.git
cd binance_A1 || exit
pip3.8 install -r requirements.txt

