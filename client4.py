# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 16:58:19 2019

@author: ajh910
"""

import socket
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities   
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.common.keys import Keys
import pymysql.cursors
import os
import requests
import datetime


##윗 PC
nm_list = ['017','018','019','020','021','022','023','024']
url = 'http://192.168.0.199/HM/?user='
driver_path = 'c:\\qa\\chromedriver.exe'

#클라이언트 화면 배치좌표
po_x = [-6, 954, -6, 954, 1914, 2874, 1914, 2874]
po_y = [-100, -100, 475, 475, -90, -90, 475, 475 ]



####크롬 세팅부터 공통모듈


#크롬세팅
_chrome_options = Options() 
_chrome_options.add_argument('disable-infobars') 
d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'browser':'ALL' }

#소켓접속주소
HOST = 'ec2-15-164-100-66.ap-northeast-2.compute.amazonaws.com'
PORT = 3838

#소켓연결

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

def ddm(x, msg): #카운트 함수, 카운트와 메시지를 동시에
    print(msg)
    for j in range(1, int(x)):
        print(str(int(x)-j))
        time.sleep(1)  
        

#서버에게 메시지 전달 
def s_msg(text):
    global client_socket
    client_socket.send(text.encode())
    
#데이터베이스 에서 좌표 읽어와서 실행하는 함수
def xy(com):    
    db = pymysql.connect(host='192.168.0.37', port=3306, user='root', passwd='pkadmin1234', db='test')
    try:
        with db.cursor() as cursor:   
            cursor.execute("SELECT title, x, y, f FROM xy_table where title = '"+com+"';")
            result0 = cursor.fetchall()
            return result0[0][1:]
    except:
        return '0'
    
    finally:
        db.close() 


#클라이언트 배치하기 / 전체 리로딩 / 개별 리로딩
def test_start(x): # 파라미터 100은 최초 시작 99는 전체 리로딩 1~8은 각자 리로딩 
    try:
        global driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8
        global nm_list
        global po_x, po_y    
        dr_list = [driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8]
        
        if x in(99, 100):
            for a,b,c,d in zip(dr_list, nm_list, po_x, po_y):
                if x == 100:
                    a.set_window_position(c,d)
                    a.set_window_size(974, 625)        
                a.get(url +'qa' + b)
                time.sleep(2)
                a.execute_script('document.getElementById("pixiCanvas").style.width = "760px"')
                a.execute_script('document.getElementById("pixiCanvas").style.height = "427px"')
                time.sleep(2)
                a.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                if x == 99:
                    print('모든 클라이언트 리로딩 합니다.')
        else:  
            x = int(x)-1
            dr_list[x].get(url +'qa' + nm_list[x])
            time.sleep(2)
            dr_list[x].execute_script('document.getElementById("pixiCanvas").style.width = "760px"')
            dr_list[x].execute_script('document.getElementById("pixiCanvas").style.height = "427px"')
            time.sleep(2)
            dr_list[x].execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except Exception as ex:
        print('에러가 발생 했습니다1\n', ex)
        

#클라이언트 종료
def test_end():
    try:
        global driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8
        dr_list = [driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8]
        for g in dr_list:
            g.quit()
        s_msg('테스트종료 완료')
    except Exception as ex:
        print('에러가 발생 했습니다1\n', ex)
 
    

#아직 미적용
        
def selector(driver_n, command): #공용 좌표 클릭 함수  # 0, 로비 = 1번클라이언트에 로비명령어를 클릭하라
    global driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8
    dr_list = [driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8]
    h = dr_list[int(driver_n)]
    xyz = xy(command)
    if xyz[2] == 0:
        ActionChains(h).move_to_element_with_offset(h.find_element_by_xpath("//*[@id='mainView']/canvas"), xyz[0], xyz[1]).click().perform() 
    elif xy[2] == 1:
        ActionChains(h).move_to_element_with_offset(h.find_element_by_xpath("//*[@id='mainView']/canvas"), xyz[0], xyz[1]).click_and_hold().perform()
        time.sleep(1)  
        ActionChains(h).move_to_element_with_offset(h.find_element_by_xpath("//*[@id='mainView']/canvas"), xyz[0], xyz[1]+5).click().perform()  
    


#각 클라이언트에 클릭 진행
def canvas_click(a,b,c):
    try:
        global driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8
        dr_list = [driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8]
    #    global driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8, driver5, driver6, driver7, driver8    
    #    dr_list = [driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8, driver5, driver6, driver7, driver8]
        for h in dr_list:
            if c == 0:
                ActionChains(h).move_to_element_with_offset(h.find_element_by_xpath("//*[@id='mainView']/canvas"), a, b).click().perform() 
            elif c == 1:
                ActionChains(h).move_to_element_with_offset(h.find_element_by_xpath("//*[@id='mainView']/canvas"), a, b).click_and_hold().perform()
                time.sleep(1)  
                ActionChains(h).move_to_element_with_offset(h.find_element_by_xpath("//*[@id='mainView']/canvas"), a, b+5).click().perform()  
    except Exception as ex:
        print('에러가 발생 했습니다2\n', ex)


#선택 클라이언트 클릭
def drc(n, x):
    try:
        n = int(n)-1
        global driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8        
        dr_list = [driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8]
        
        if x[2] == 1:
            ActionChains(dr_list[n]).move_to_element_with_offset(dr_list[n].find_element_by_xpath("//*[@id='mainView']/canvas"), x[0], x[1]).click_and_hold().perform()
            time.sleep(1)  
            ActionChains(dr_list[n]).move_to_element_with_offset(dr_list[n].find_element_by_xpath("//*[@id='mainView']/canvas"), x[0], x[1]+5).click().perform()         
        elif x[2] == 0:
            ActionChains(dr_list[n]).move_to_element_with_offset(dr_list[n].find_element_by_xpath("//*[@id='mainView']/canvas"), x[0], x[1]).click().perform()             
    except Exception as ex:
        print('에러가 발생 했습니다4\n', ex)


#클라이언트 팝업 # 0은 전체, 개별은 개별 번호 
def drc_p(n):
    try:
        global driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8
        n = int(n)-1
        dr_list = [driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8]
        lst = [
        ['1번째구매',  588, 83],
        ['스페셜 딜 ',  612, 42],
        ['뉴슬롯    ',  594, 59],
        ['핀투탑    ',  612, 42],
        ['입장창닫기',  635, 59],
        ]
        if n == -1: #전체 팝업 닫기            
            for z in lst:
                canvas_click(z[1], z[2], 0)
        else:
            for z in lst:
                ActionChains(dr_list[n]).move_to_element_with_offset(dr_list[n].find_element_by_xpath("//*[@id='mainView']/canvas"), z[1], z[2]).click().perform()         
    except Exception as ex:
        print('에러가 발생 했습니다6\n', ex)
        
#개별 클라이언트 반복
def inging(dr, y, n): #개별 반복 #클라 명령어 횟수 #############################
    try:
        global driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8
        dr_list = [driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8]
        dr = int(dr)-1        
        x = xy(y)        
        for i in range(0, int(n)+1):
            if x[2] == 1:
                ActionChains(dr_list[dr]).move_to_element_with_offset(dr_list[dr].find_element_by_xpath("//*[@id='mainView']/canvas"), x[0], x[1]).click_and_hold().perform()
                time.sleep(1)  
                ActionChains(dr_list[dr]).move_to_element_with_offset(dr_list[dr].find_element_by_xpath("//*[@id='mainView']/canvas"), x[0], x[1]+5).click().perform()         
            elif x[2] == 0:
                ActionChains(dr_list[dr]).move_to_element_with_offset(dr_list[dr].find_element_by_xpath("//*[@id='mainView']/canvas"), x[0], x[1]).click().perform() 
    
    except Exception as ex:
        print('에러가 발생 했습니다7\n', ex)


#개별 클라이언트 진행(순서대로)
def sunse(dr, y): #개별 클라, 명령어     #############################
    dr = int(dr)-1
    try:        
        global driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8
        dr_list = [driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8]
        for i in y:
            x = xy(i)            
            if x[2] == 1:
                ActionChains(dr_list[dr]).move_to_element_with_offset(dr_list[dr].find_element_by_xpath("//*[@id='mainView']/canvas"), x[0], x[1]).click_and_hold().perform()
                time.sleep(1)  
                ActionChains(dr_list[dr]).move_to_element_with_offset(dr_list[dr].find_element_by_xpath("//*[@id='mainView']/canvas"), x[0], x[1]+5).click().perform()         
            elif x[2] == 0:
                ActionChains(dr_list[dr]).move_to_element_with_offset(dr_list[dr].find_element_by_xpath("//*[@id='mainView']/canvas"), x[0], x[1]).click().perform()  
            time.sleep(5)
            
    except Exception as ex:
        print('에러가 발생 했습니다8\n', ex)

    
##### =============================================================================

print('- 클라이언트 서버에 접속 완료!\n수신 대기중 ...')

while True:
    try:
        client_socket.connect((HOST, PORT))
        break
    except:
        ddm(10, '10초 뒤 재접속 시도합니다.')
        time.sleep(3)
        pass


##### =============================================================================
        
    
while True:
    msg = client_socket.recv(1024).decode()        
    msg = msg[msg.find(']')+2:]
    print(msg)
    
    if msg == '테스트시작':        
        #글로벌 변수선언
        for i in range(1, 9):        
            globals()['driver{}'.format(i)] = webdriver.Chrome(driver_path,  chrome_options=_chrome_options)
        
        dr_list = [driver1, driver2, driver3, driver4, driver5, driver6, driver7, driver8]        
        test_start(100)
        s_msg('클라이언트 세팅 완료')
        
    elif msg == '연결종료':        
        break
        
    elif msg == '리로딩':
        test_start(99)
        s_msg('클라이언트 리로딩 완료')        
        
    elif msg == '테스트종료':
        test_end()
        s_msg('테스트 종료 완료')                
        
    elif msg == '팝업':
        drc_p(0)
        s_msg('팝업 닫기 완료')
        
    elif msg =='스샷':
        try:
            nnow = datetime.datetime.now().strftime("%y%m%d%H%M%S")
            driver1.save_screenshot(r'c:\\qa\\'+nnow+'_client2.png') #선택 클라이언트 클릭
            ## 파일 올리기 
            urll = 'http://192.168.0.37:8000/fileUpload'
            files = {'file1': open(r'c:\\qa\\'+nnow+'_client2.png', 'rb')}
            r = requests.post(urll, files=files)
            
            s_msg('스크린샷 및 서버로 전송 완료')        
        except Exception as ex:
            print('에러가 발생 했습니다8\n', ex)
        
    else: #설정된 메시지 외 다른게 들어왔을 때
        if xy(msg) != '0': #DB에 명령어가 있을 경우 진행
            pp = xy(msg)
            canvas_click(pp[0], pp[1], pp[2])
            s_msg(msg +' 클릭 실행 완료!!')            
            
        else: #DB에 명령어가 없을경우는 진행 and 띄어쓰기가 있을 경우 진행
            try:
                if len(msg.split(' ')) >= 2:
                    
                    if msg.split(' ')[0] =='뒤': #개별 클라 실행
                        try:
                            q = msg.split(' ')[2]                        
                        except:
                            q = ''    
                        if q == '리로딩':# 개별 리로딩 // 클라 1 리로딩딩
                            test_start(msg.split(' ')[1])
                            s_msg('개별 리로딩 실행 완료!!')                        
                            
                        elif q == '팝업':# 개별 팝업 // 클라 1 팝업
                            drc_p(msg.split(' ')[1])
                            s_msg('개별 팝업 실행 완료!!')                        
                       
                        elif q == '반복': #반복클릭 // ㅋ 1 반복 배팅하 5
                            print('반복명령어 나열 : ' + msg.split(' ')[1]+' - ' + msg.split(' ')[3]+' - ' + msg.split(' ')[4])
                            inging(str(msg.split(' ')[1]), str(msg.split(' ')[3]), str(msg.split(' ')[4]))#클라, 명령어, 횟수
                            s_msg('개별 반복 실행 완료')                        
                            
                        elif q == '진행': # 빈행클릭  // ㅋ 1 반복 로비 사이드메뉴 사이드1 슬롯1 플레이
                            print('진행명령어 나열 : ' + msg.split(' ')[1]+' - ' + msg.split(' ')[3])
                            sunse(msg.split(' ')[1], msg.split(' ')[3:]) #클라명, 명령어들                        
                            s_msg('개별 진행 실행 완료')                        
                            
                        else: #일반 클릭 //클라 1 로비 / 롱 숏 모두 포함                        
                            drc(msg.split(' ')[1], xy(q))
                            s_msg('개별 클릭 실행 완료')                        
                            
                        
                    elif msg.split(' ')[0] =='반복': #전체 클라이언트 // 반복 로비 4
                        pp = xy(msg.split(' ')[1])
                        for w in range(0, int(msg.split(' ')[2]) +1):
                            canvas_click(pp[0], pp[1], pp[2])
                            s_msg('전체 클라 클릭 실행 완료')
                            
                    elif msg.split(' ')[0] =='진행': #전체 클라이언트 진행 // 진행 로비 사이드메뉴 사이드1 슬롯1 플레이                    
                        if msg[len(msg)-1:] == ' ':
                            msg = msg[0:len(msg)-1]                    
                        for q in msg.split(' ')[1:]:
                            pp = xy(q)
                            canvas_click(pp[0], pp[1], pp[2])
                            time.sleep(5)                        
                        s_msg('전체 클라 진행 클릭 완료')                 
                        
            except:
                print('명령어가 없습니다.1')
                pass
client_socket.close()
print('소켓 연결이 종료되었습니다.')
time.sleep(3)
os._exit(0)