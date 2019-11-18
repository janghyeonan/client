# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 14:33:08 2019

@author: ajh910 
"""
import socket 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities   
import time
import os
import datetime

##윗 PC
url = 'https://blog.naver.com/ajh910'
driver_path = 'c:\\renardy\\chromedriver.exe'


#크롬세팅
_chrome_options = Options() 
_chrome_options.add_argument('disable-infobars') 
d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'browser':'ALL' }

#소켓접속주소
HOST = '192.168.0.12'
PORT = 9997

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
    msg = client_socket.recv(1024).decode()        
    print('받은 메시지 : '+msg)
    
    if msg == '테스트시작':        
        #글로벌 변수선언
        driver = webdriver.Chrome(driver_path,  chrome_options=_chrome_options)
        driver.get(url)
        s_msg('클라이언트 세팅 완료')
        
    elif msg == '테스트종료':
        driver.quit()
        
    elif msg == '연결종료':        
        break
        
    elif msg =='스샷':
        try:
            nnow = datetime.datetime.now().strftime("%y%m%d%H%M%S")
            driver.save_screenshot(r'c:\\renardy\\'+nnow+'_screenshot.png')
                        
            s_msg('스크린샷 완료')        
        except Exception as ex:
            print('에러가 발생 했습니다8\n', ex)
        
    else: #설정된 메시지 외 다른게 들어왔을 때
        s_msg('명령어 목록이 없습니다.')
         
client_socket.close()
print('소켓 연결이 종료되었습니다.')
time.sleep(3)
os._exit(0)