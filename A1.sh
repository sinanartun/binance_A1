#!/bin/bash
sudo yum update -y
sudo yum upgrade -y
cd /home/ec2-user || exit
sudo amazon-linux-extras enable python3.8
sudo amazon-linux-extras install epel -y
yum clean metadata
sudo yum install htop -y
sudo yum install python3.8 -y
curl -O https://bootstrap.pypa.io/get-pip.py
python3.8 get-pip.py --user
sudo yum install git -y
git clone https://github.com/sinanartun/binance_A1.git
sudo chown -R ec2-user:ec2-user /home/ec2-user/binance_A1
sudo chmod 2775 /home/ec2-user/binance_A1 && find /home/ec2-user/binance_A1 -type d -exec sudo chmod 2775 {} \;
cd binance_A1 || exit
pip3.8 install -r requirements.txt
{
  echo "export AccessKeyId='XXXX'";
  echo "export SecretAccessKey='XXX'";
  echo "export bucket_name='XXX'";
  echo "export region='XXX'"
}>> /home/ec2-user/.bash_profile

source /home/ec2-user/.bash_profile
python3.8 main.py