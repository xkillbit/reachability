# reachability
THIS IS PYTHON WRAPPED AROUND MASSCAN
# -- START DISCLAIMER --

# USE AT OWN RISK -- IN NO WAY AM I RESPONSIBLE FOR ANY DAMAGES INCURRED -- IF YOU DON'T HAVE EXPLICT PERMISSION BY THE NETWORK OWNER DO NOT AND I REPEAT DO NOT LAUNCH THIS 

THIS IS PYTHON WRAPPED AROUND MASSCAN (https://github.com/robertdavidgraham/masscan)
# -- END DISCLAIMER--

These scripts assume you are on a debian linux distro and have internet access.

# Questions the script answers?

Are the target ranges reachable? If so how many in each range? If that isn't enough, what IP addresses are responding and on which ports?

# Scenerios
1. You are given access to a network or set of networks and you are told to pen test team. To verify you have access to all ranges you must go through a process of ping sweeping and port scanning then comparing your IP address that returned open ports or responded to pings to determine which ranges you have access to. Sometimes the list of ranges is pages long. This script solves the problem of manual cross comparison between the results of scan data and the list of CIDR ranges for which you are supposed to be granted access. Many times you don't get access to everything in the first go around and this process is time consuming.

2. You are on a Pen Test or you are simply assigned the task of ensuring that proper network segmentation is in place between a list of networks. This script makes it a simple and easy process with excel output evidence for the management overlords.

# reachy.py
# EASYMODE - COPY/PASTA (into your terminal):
[WARNING : DO NOT RUN ON A CORP Attached Network unless you are meaning too. ]
This command will download the tool, set it up, and run it on the first network interface you are attached to as a /24.
> sudo git clone https://github.com/xkillbit/reachability.git && cd reachability&&sudo chmod 755 setup.sh && sudo ./setup.sh && echo ' ' && echo ' '&& echo '**Create a file named targets.list (or whatever you would like to name the file), fill it with line seperate IP ranges in CIDR notation such as 192.168.0.0/24 then run $>./ireach.py to continue life on easy street**'

# MANUAL MODE:

>sudo git clone https://github.com/xkillbit/reachability.git

>cd reachability

>sudo chmod 755 setup.sh

> sudo ./setup.sh

(This script makes sure you have everything you need to run reachy.py)

Create a line seperated list of target IP Ranges (IE: x.x.x.x/24).
> echo "127.0.0.1/32" >> targets.list
> 
> echo "192.168.1.1/32" >> targets.list

Fire at will:
>sudo ./reachy.py targets.list




# FOLLOW THE DOGE TO WATCH THE DEMO (click on the dog)
[![Watch the video](https://i.imgur.com/EVvpwLb.jpg)](https://youtu.be/VHPm6h8ZAeM)
