# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 16:58:19 2019

@author: ajh910
"""

import socket
from threading import Thread

HOST = 'localhost'
PORT = 9009

def rcvMsg(sock):
   while True:
      try:
         data = sock.recv(1024)
         if not data:
            break
         print(data.decode().split(' ')[1])        
      except:
         pass

def runChat():
   with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
      sock.connect((HOST, PORT))
      t = Thread(target=rcvMsg, args=(sock,))
      t.daemon = True
      t.start()

      while True:
         msg = input('메시지를 입력하세요. : ')
         if msg == '/exit':
            sock.send(msg.encode())
            break        
         sock.send(msg.encode())
            
runChat()