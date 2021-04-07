#! /bin/bash
echo '--------------THIS MUST BE RUN AS ROOT--------------'
apt update
apt install masscan
apt install -y sed
apt install -y python3
apt install -y python3-pip
python3 -m pip install --upgrade pip setuptools
pip3 install python-masscan
pip3 install tabulate
pip3 install ipaddress
pip3 install pandas
pip3 install PyInquirer
updatedb
sed -i 's/logger.debug/#&/' $(locate masscan.py)
chmod 755 reachy.py
chmod 755 ireachy.py
