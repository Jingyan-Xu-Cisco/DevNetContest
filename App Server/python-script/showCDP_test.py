#!/usr/bin/env python3
import json
import time
import datetime

from threading import Thread
from netmiko import ConnectHandler

class MyThread(Thread):
    def __init__(self, func, args):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None

def get_cdp_neighbors(Sw):
    try:
        print (f'Login {Sw} and show cdp neighbors!')
        device = {
            "device_type": "cisco_ios_telnet",
            "host": "Initial value",
            "username": user,
            "password": password,
            "secret": password,
            "port": 23,
        }
        device["host"] = Sw
        c = ConnectHandler (**device)
        c.enable ()
        cdp_neighbors = c.send_command('show cdp neighbors', use_textfsm = True)
        cdp_result_json = cdp_neighbors
        hostname = c.send_command('sh run | i host').split()[1]
#       print (json.dumps (cdp_neighbors, indent = 2))
        c.disconnect ()
        cdp_result = {
            "hostname": hostname,
            "ip": Sw,
            "cdp_result": cdp_result_json
        }
    except Exception as ex:
        print (ex)
        cdp_result = {
            "hostname": "",
            "ip": Sw,
            "cdp_result": []        
        }
#    print (json.dumps (cdp_result, indent = 2))
    return cdp_result

def get_all_neighbors(Sw_IP):
    cdp_list = []
    cdp_results = []
    device_name_list = []
    for Sw in Sw_IP:
        t = MyThread(get_cdp_neighbors, (Sw, ))
        cdp_list.append(t)
        t.start()
    for t in cdp_list:
        t.join()
        cdp_results.append(t.get_result())
    return cdp_results

def data_collation(data):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    result = []
    device_name_list = []
    # get device name list
    for cell in data:
        device_name_list.append(cell["hostname"])
    # cdp data collcation
    for cell in data:
        hostname = cell["hostname"]
        ip = cell["ip"]
        cdp_result = cell["cdp_result"]
        for cdp in cdp_result:
            if cdp["neighbor"] in device_name_list:
                tmp_cell = (hostname, ip, cdp['local_interface'], cdp["neighbor"], cdp["neighbor_interface"], timestamp)
                result.append(tmp_cell)
    return result

def save_to_db(data):
    print (json.dumps (data, indent = 2))
    import mysql.connector as mariadb
    conn = mariadb.connect(
          host="10.80.9.1",
          user="remote",
          password="C1sc0123",
          database="TLPR_test"
        )
    cursor = conn.cursor()
    sql_select_Query = "INSERT IGNORE INTO CDP_table (local_device_name, local_device_ip, local_interface, remote_device_name, remote_interface, time) VALUES (%s, %s, %s, %s, %s, %s)"
#    sql_select_Query = "INSERT IGNORE INTO CDP_test (local_device_name, local_device_ip, local_interface, remote_device_name, remote_interface, time) VALUES (%s, %s, %s, %s, %s, " + '"' + timestamp + '"' + ")"
    print (sql_select_Query)
    cursor.executemany(sql_select_Query,data)
    conn.commit()
    print(cursor.rowcount, "Saved DB successfully!")


def main():
    # get cdp neighbors
    cdp_results = get_all_neighbors(Sw_IP)
    cdp_list = data_collation(cdp_results)

    # save to db
    save_to_db(cdp_list)


    

if __name__ == '__main__':
    user = "admin"
    password = "C1sc0123"
    Sw_IP = [
        "10.80.100.41",
        "10.80.100.42",
        "10.80.100.43",
    ]
    main()
