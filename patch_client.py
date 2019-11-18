# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 14:33:08 2019

@author: ajh910
"""
import socket 
import requests
import subprocess
import os
import time

print('패치 서버 접속 대기중...')
#소켓접속주소
HOST = '192.168.0.37'
PORT = 9999
#소켓연결

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
client_socket.connect((HOST, PORT)) 


#서버에게 메시지 전달 
def s_msg(text):
    print(text)
    global client_socket
    client_socket.send(text.encode())
  
print('- 클라이언트 서버에 접속 완료!\n수신 대기중 ...')

while True: 
    try:
        msg = client_socket.recv(1024).decode()        
        print('받은 메시지 : '+msg)
        
        if msg == '패치시작':
            url = 'http://192.168.0.37:8000/static/client1.pyp'
            r = requests.get(url, allow_redirects=True)
            open(r'c:\\qa\\client1.py', 'wb').write(r.content)
            print('클라1 다운로드 완료!')
            
            url1 = 'http://192.168.0.37:8000/static/client2.pyp'
            r1 = requests.get(url1, allow_redirects=True)
            open(r'c:\\qa\\client2.py', 'wb').write(r1.content)
            print('클라2 다운로드 완료!')
            
            url2 = 'http://192.168.0.37:8000/static/client3.pyp'
            r2 = requests.get(url2, allow_redirects=True)
            open(r'c:\\qa\\client3.py', 'wb').write(r2.content)
            print('클라3 다운로드 완료!')
            
            url3 = 'http://192.168.0.37:8000/static/patch_client.pyp'
            r3 = requests.get(url3, allow_redirects=True)
            open(r'c:\\qa\\patch_client.py', 'wb').write(r3.content)
            print('패치클라이언 완료!')
        elif msg =='클라실행':
            subprocess.Popen(r'c:\\remote_client.bat', creationflags=subprocess.CREATE_NEW_CONSOLE)
        elif msg =='연결종료':
            break
            
    except Exception as ex:
        print('에러가 발생 했습니다', ex)

client_socket.close()
print('소켓 연결이 종료되었습니다.')
time.sleep(3)
os._exit(0)