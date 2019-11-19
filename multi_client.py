# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 16:58:19 2019

@author: ajh910
"""

import socket
import os
import time

HOST = 'localhost'
PORT = 9009

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

def ddm(x, msg): #카운트 함수, 카운트와 메시지를 동시에
    print(msg)
    for j in range(1, int(x)):
        print(str(int(x)-j))
        time.sleep(1)  
while True:
    try:
        client_socket.connect((HOST, PORT))
        break
    except:
        ddm(10, '10초 뒤 재접속 시도합니다.')
        time.sleep(3)
        pass

while True:
    try:
        msg = client_socket.recv(1024).decode()        
        print(msg.split(' ')[1])
        if msg.split(' ')[1] =='세기':
            for i in range(0, 21):
                print(i)
        elif msg.split(' ')[1] =='종료':
            break
    except KeyboardInterrupt:
        break
    
client_socket.close()    
os._exit(0)