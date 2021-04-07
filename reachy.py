#! /usr/bin/python3
import time
import datetime 
import sys
import masscan
import pandas as pd
import ipaddress
import os
from tabulate import tabulate
from collections import OrderedDict
if len(sys.argv) == 2:
    print("You are scanning ranges in file named: ",sys.argv[1])
elif len(sys.argv) == 3:
    print("You are scanning at your selected rate of: ", sys.argv[2], " packets per second.")
else:
    print('MUST RUN AS ROOT!!! No SUDO!!!\nUSAGE: ./reachy.py [TARGET_RANGES_LINE_SEPERATED_LIST_FILE_NAME] [CUSTOM RATE, ELSE 10k PPS by DEFAULT]\n\n\n')
    
print('\nScanning from:\n')
os.system("ip -br -c address|grep -v lo")
time.sleep(1)

def get_ranges():
    list_of_ip_ranges=[]
    string_ranges=[]
    f = open(sys.argv[1], 'r')
    for eachRange in f:
        string_ranges.append(eachRange.strip("\s\n\t\r"))
        list_of_ip_ranges.append(ipaddress.ip_network(eachRange.strip("\s\n\t\r"),False))

    f.close()
    return [string_ranges,list_of_ip_ranges]

my_ranges = get_ranges()
scan_resultz={}

# range results will be KEY: IP RANGE, VALUES: list_of_up_hosts
range_resultz={}
nm = masscan.PortScanner()
# SCAN TOP 100 Ports
#Check if user passes a rate. If no rate then DEFAULT SCAN RATE IS SET TO 10K/PacketsPerSecond
if len(sys.argv) == 3:
    nm.scan(str(my_ranges[0]).strip("[]"), ports='7,9,13,21-23,25-26,37,53,79-81,88,106,110-111,113,119,135,139,143-144,179,199,389,427,443-445,465,513-515,543-544,548,554,587,631,646,873,990,993,995,1025-1029,1110,1433,1720,1723,1755,1900,2000-2001,2049,2121,2717,3000,3128,3306,3389,3986,4899,5000,5009,5051,5060,5101,5190,5357,5432,5631,5666,5800,5900,6000-6001,6646,7070,8000,8008-8009,8080-8081,8443,8888,9100,9999-10000,32768,49152-49157',arguments="--max-rate"+' '+str(sys.argv[2]))
#if rate is NOT given by user then use default 10k PPS
else:
    nm.scan(str(my_ranges[0]).strip("[]"), ports='7,9,13,21-23,25-26,37,53,79-81,88,106,110-111,113,119,135,139,143-144,179,199,389,427,443-445,465,513-515,543-544,548,554,587,631,646,873,990,993,995,1025-1029,1110,1433,1720,1723,1755,1900,2000-2001,2049,2121,2717,3000,3128,3306,3389,3986,4899,5000,5009,5051,5060,5101,5190,5357,5432,5631,5666,5800,5900,6000-6001,6646,7070,8000,8008-8009,8080-8081,8443,8888,9100,9999-10000,32768,49152-49157',arguments='--max-rate 100')



#initalize  counts of each value to zero in range_resultz dict
for eachRange in my_ranges[1]:
    range_resultz[eachRange] = 0

#Create a dict of IP Address that responded with open ports
for eachIP in nm.scan_result['scan'].keys():
    for eachProto in nm.scan_result['scan'][eachIP]:
        portz=nm.scan_result['scan'][eachIP][eachProto].keys()
        scan_resultz[ipaddress.ip_address(eachIP)] = [eachProto, sorted(list(portz))]

#Count IPs in Ranges
for eachRange in my_ranges[1]:
    for eachIP in scan_resultz.keys():
        if eachIP in eachRange.hosts():
            range_resultz[eachRange]=range_resultz[eachRange]+1
    
sorted_resultz=OrderedDict(scan_resultz)
df = pd.Series(sorted_resultz)

# Convert all values in range results to strings for printing purposes
for k,v in range_resultz.items():
    range_resultz[k]=str(v)
    
#print(range_resultz)
df2 = pd.Series(range_resultz)
print(tabulate(df2.sort_values(),headers=('IP Range', 'Live Nodes'),tablefmt='grid'))
content2 =tabulate(df2.sort_values(),headers=('IP Range','Live Nodes'),tablefmt='tsv')

 

# PRINT Indivdual IP Address and associate up ports TO SCREEN
print(tabulate(df.sort_index(),headers=('IP Address','Protocol','Open Ports'),tablefmt='grid'))
content = tabulate(df.sort_index(),headers=('IP Address','Protocol','Open Ports'),tablefmt='tsv')
filename = 'logs/reachy-outfile-run-on-%s.tsv'%datetime.datetime.now().strftime('%Y-%m-%d-%H%M')
text_file2=open(filename,'w')
text_file2.write(content2)
text_file2.close()

text_file= open(filename,'a')
text_file.write('\n\n'+content)
text_file.close()

print("\nTables are saved as:\t\t\t\t",filename,'\n')

# Create a list for importing into nessus as targets for next round of scans
other_filename = 'logs/reachy-uphosts-run-on-%s.list'%datetime.datetime.now().strftime('%Y-%m-%d-%H%M')
text_file3 = open(other_filename,'w')

sort_my_list=[]
for eachIP in nm.scan_result['scan'].keys():
    sortme=ipaddress.ip_address(eachIP)
    sort_my_list.append(sortme)

return_sorted_ips_to_strings=[]
for eachIP in sorted(sort_my_list):
    return_sorted_ips_to_strings.append(str(eachIP))
    
for eachIP in return_sorted_ips_to_strings:
    text_file3.write(eachIP+'\n')

text_file3.close()

print("List file of up-hosts saved as:\t\t\t", other_filename,'\n\n')




