#!/usr/bin/env python3
import re
import base64
import urllib.request
import os, shutil
import socket

# Create folder
vpn_dir = 'VPN'
if os.path.exists(vpn_dir):
    shutil.rmtree(vpn_dir)
os.makedirs(vpn_dir)

# Create vpn's
url = 'http://www.vpngate.net/api/iphone/'
count = 0
response = urllib.request.urlopen(url)
for line in response:
    line_decoded = line.decode('utf-8')
    if( "owner" in line_decoded):
        line_striped = re.sub("^vpn.*owner,,","",line_decoded).strip()
        try:
                # Decode line
                ovpn_text = base64.b64decode(line_striped).decode("utf-8")
                # Delete comments
                ovpn_text = re.sub("(#|;).*\n","" ,ovpn_text)
                title = str(count)+".ovpn"
                ovpn_file = open(vpn_dir+"/"+title, 'w')
                ovpn_file.write(ovpn_text)
                ovpn_file.close()
                count += 1
        except:
                print("Fallo")

# Delete powered off servers
for filename in os.listdir(vpn_dir):
        ovpn_file = open(vpn_dir+"/"+filename, 'r')
        for line in ovpn_file.readlines():
                if "remote" in line:
                        server = line.strip().split(" ")
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1)
                        result = sock.connect_ex((server[1],int(server[2])))
                        if result == 0:
                                print("Server "+str(server[1])+":"+str(server[2])+" ON")
                        else:
                                print("Server "+str(server[1])+":"+str(server[2])+" OFF, borrando")
                                os.remove(vpn_dir+"/"+filename)

