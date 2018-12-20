#!/bin/python3

import telnetlib
import json

servers = open("servers.txt", 'w')
servers.truncate()
server_list =  open('servers.json', 'r')
server_json = json.load(server_list)
for key in server_json['matches']:
    servers.write(key["ip_str"]+"\n")
#    print(key["ip_str"])
servers.close()

servers = open("servers.txt", 'r')
alive_servers = open("alive-servers.txt", 'w')
alive_servers.truncate()

for ip in servers.readlines():
        ip = ip.strip()
        try:
            tn = telnetlib.Telnet(ip, 11211,2)
            tn.write(b"version\r\n")
            version = tn.read_some().decode('ascii').split()
            tn.close()
#            print(version)
            versionnumber = version[1].split(".")
            n = int(versionnumber[1])
            if n < 5:
                print(ip+" "+str(version))
                alive_servers.write(ip+"\n")
        except Exception as err:
            print(err)
            pass
