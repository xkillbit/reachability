from encodings import utf_8
import optparse
import datetime
import ipaddress
import os
import time
from collections import OrderedDict
from turtle import speed
import masscan
import pandas as pd
from tabulate import tabulate

parser = optparse.OptionParser()
parser.add_option("-t", "--targets-file", dest='target_file',
        help="search your term") 
parser.add_option("-s", "--speed-pps", dest='scan_speed',
        help="search your term") 
parser.add_option("-i", "--interface", dest='interface',
help="search your term") 
parser.add_option("-p", "--top-ports", dest='top_ports_count',
help="search your term") 

(options,args) = parser.parse_args()

if options.target_file == None:
    print(parser.usage)
    exit(0)
else:
    target_file = options.target_file

if options.scan_speed == None:
    scan_speed = 10000 #Set Default Speed 10,000 pps
else:
    scan_speed = options.scan_speed

if options.interface == None:
    interface = 'eth0' #default interface is eth0
else:
    interface = options.interface

if options.top_ports_count == None:
    top_ports_count = '10' #default top ten ports
else:
    top_ports_count = options.top_ports_count



def get_ranges(target_file):
    list_of_ip_ranges=[]
    string_ranges=[]
    characters = "\n"
    with open(target_file,'r',encoding='utf-16') as f:
        for eachRange in f:
            if eachRange:
                string_ranges.append(eachRange.strip(characters))
                list_of_ip_ranges.append(ipaddress.ip_network(eachRange.strip(characters),False))

            #list_of_ip_ranges.append(ipaddress.ip_network(eachRange,False))
    #ranges = (set(zip(string_ranges,list_of_ip_ranges)))
    #print(string_ranges)
    range_dict = {string_ranges: list_of_ip_ranges for string_ranges,
                  list_of_ip_ranges in zip(string_ranges,list_of_ip_ranges)            
    }
    #print(range_dict)
    return range_dict

def run_scan(ip_ranges):
    nm = masscan.PortScanner()
    if target_file and scan_speed:
        ip_range_list = []
        for k in ip_ranges.keys():
            #print("Value: {} -- Type: {}".format(v,type(v)))
            ip_range_list.append(k)
        ip_ranges_str = ','.join(ip_range_list)
        nm.scan(ip_ranges_str,arguments="-e {} --top-ports {} --max-rate {}".format(interface,top_ports_count,scan_speed))

def get_ip_count(zranges):
    scan_resultz={}
    range_count_resultz = {}
    #initalize  counts of each value to zero in range_count_resultz dict
    for eachRange in zranges.keys():
        range_count_resultz[eachRange] = 0
    #Create a dict of IP Address that responded with open ports
    for eachIP in nm.scan_result['scan'].keys():
        for eachProto in nm.scan_result['scan'][eachIP]:
            portz=nm.scan_result['scan'][eachIP][eachProto].keys()
            scan_resultz[ipaddress.ip_address(eachIP)] = [eachProto, sorted(list(portz))]
    #Count IPs in Ranges
    for eachRange in zranges.keys():
        for eachIP in scan_resultz.keys():
            if eachIP in eachRange.hosts():
                range_count_resultz[eachRange]=range_count_resultz[eachRange]+1
    return range_count_resultz,scan_resultz

def get_uphosts():
    scan_resultz = {}
    for eachIP in nm.scan_result['scan'].keys():
        for eachProto in nm.scan_result['scan'][eachIP]:
            portz=nm.scan_result['scan'][eachIP][eachProto].keys()
            scan_resultz[ipaddress.ip_address(eachIP)] = [eachProto, sorted(list(portz))]
    return scan_resultz
    

# LOGIC
range_dict = get_ranges(target_file)
run_scan(range_dict)