import os
import json
from netmiko import ConnectHandler

user = 'admin'
password = 'C1sc0123'
Sw1_IP = '10.80.100.41'
Sw2_IP = '10.80.100.42'
Sw3_IP = '10.80.100.43'

device = {
    "device_type": "cisco_ios_telnet",
    "host": Sw1_IP,
    "username": user,
    "password": password,
    "secret": password,
    "port": 23,
}

try:
    c = ConnectHandler (**device)
    c.enable ()
    interfaces = c.send_command('show ip int brief', use_textfsm = True)
    print (json.dumps (interfaces, indent = 2))
    c.close ()
except Exception as e:
    print (e)
