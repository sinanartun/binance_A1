#!/bin/bash
sudo amazon-linux-extras enable python3.8
yum clean metadata
sudo yum install python3.8 -y
curl -O https://bootstrap.pypa.io/get-pip.py
python3.8 get-pip.py --user
sudo yum install git -y
