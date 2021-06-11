#!/usr/bin/env python3
import json
from netmiko import ConnectHandler

user = "admin"
password = "C1sc0123"
Sw_IP = [
    "10.80.100.41",
    "10.80.100.42",
    "10.80.100.43",
]

device = {
    "device_type": "cisco_ios_telnet",
    "host": "Initial value",
    "username": user,
    "password": password,
    "secret": password,
    "port": 23,
}

try:
    for Sw in Sw_IP:
       print (f'{Sw}')
       device["host"] = Sw
       c = ConnectHandler (**device)
       c.enable ()
       cdp_neighbors = c.send_command('show cdp neighbors', use_textfsm = True)
       print (json.dumps (cdp_neighbors, indent = 2))
       c.disconnect ()
except Exception as e:
    print (e)
