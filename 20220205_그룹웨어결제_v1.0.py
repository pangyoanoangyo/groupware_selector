from selenium import webdriver
from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert #팝업창을 활용하는 임포트

from tkinter import *
from tkinter import font
import tkinter.messagebox as msgbox

# Tkinter의 시작
root = Tk()
root.title("자동결제 v1.0.0") # 윈도우 상단의 이름
root.geometry("250x100") # 가로 * 세로 ("640x480+300+100") # 가로 * 세로 + x좌표 + y좌표
root.resizable(False, False) # x(너비), y(높이) 높이 변경불가

# 코드속 색상표 
BLACK = "#000000"
IDIS_COLOR = "#0099b0"

# 코드 속 폰트
f10 = font.Font(family="Sandoll 맑은고딕", size=10,weight='bold')
f12 = font.Font(family="Sandoll 맑은고딕", size=12,weight='bold')
f15 = font.Font(family="Sandoll 맑은고딕", size=15,weight='bold')

# 라벨만들기 함수
def lbl(name,frame,font_size,font_color,text_in,r,c,px,py):  #name은 str로 해야한다.
    name = Label(frame,font=font_size,fg=font_color,text=text_in)
    name.grid(row=r,column=c,padx=px,pady=py,sticky=N+E+W+S)
    
    # # entry만들기 함수
# def ent(e_name,frame,넓이,r,c,px,py,text_in):
#     e_name = Entry(frame, width=넓이)
#     e_name.insert(END, text_in)
#     e_name.grid(row=r,column=c,padx=px, pady=py, sticky=N+E+W+S)

def btn_cmd():  
    options = webdriver.ChromeOptions() #로그를 없애는 거니까 안해도 된다. 필요없는 에러로그 나오는게 보기 싫어서 써준 코드
    options.add_experimental_option("excludeSwitches", ["enable-logging"]) 
    # driver = webdriver.Chrome(executable_path="D:\00000.개발의 귀재\PJT_2022\그룹웨어 결제기\chromedriver.exe")
    driver = webdriver.Chrome(options=options) # 경로지정을 안했다고 지랄해서, 파일전달할때 구글드라이버도 같이 전달
    driver.get("https://gw.idis.co.kr")
    
    frame_move_1 = driver.find_element_by_name("content") #frame안에 frame src이 있어서 들어가야한다.content라는 name으로 되어있다.
    driver.switch_to.frame(frame_move_1) #프레임 이동으로 이동한다

    driver.find_element_by_id("uid").send_keys("{0}".format(entry_1.get())) # id입력
    driver.find_element_by_id("upw").send_keys("{0}".format(entry_2.get())) # pw입력
    driver.find_element_by_css_selector(".btn_area").click() #클릭하여 로그인 이동
    
    if len(entry_1.get()) == 0:
        msgbox.showwarning("경고", "아이디를 입력하세요")
        return
    if len(entry_2.get()) == 0:
        msgbox.showwarning("경고", "암호를 입력하세요")
        return
    
    driver.find_element_by_css_selector(".napproval").click() #클릭하여 이동 (전자결제)

    frame_move_2 = driver.find_element_by_name("ibody") #frame안에 frame src이 있어서 들어가야한다.ibody라는 name으로 되어있다.
    driver.switch_to.frame(frame_move_2) #프레임 이동으로 이동한다

    frame_move_3 = driver.find_element_by_name("iframe_content") #frame안에 frame src이 있어서 들어가야한다.iframe_content라는 name으로 되어있다.
    driver.switch_to.frame(frame_move_3) #프레임 이동으로 이동한다

    # driver.find_element_by_class_name("sub_title").click() #클릭하여 이동 (진행중인 문서)
    driver.find_element_by_xpath('//*[@id="list_body"]/table/tbody/tr[1]/td[2]/div/span').click() #클릭하여 이동 (회계전표)

    frame_move_4 = driver.find_element_by_name("docframe") #frame안에 frame src이 있어서 들어가야한다.docframe라는 name으로 되어있다.
    driver.switch_to.frame(frame_move_4) #프레임 이동으로 이동한다
    driver.find_element_by_class_name('btn_blue_r').click() #클릭하여 이동 (결제)

    driver.switch_to.window("_win_aprv_process")
    Alert(driver).dismiss()  # Alert(팝업창) 거절 누름


    driver.find_element_by_xpath('//*[@id="list_body"]/table/tbody/tr[2]/td[2]/div/span').click() 
    driver.find_element_by_class_name('btn_blue_r').click() 
    Alert(driver).accept()  # Alert(팝업창) 수락 누름
    # Alert(driver).dismiss()  # Alert(팝업창) 거절 누름
    # driver.find_element_by_xpath('//*[@id="confirm"]/span').click() #결제창에서 취소
    
    driver.switch_to.default_content() #처음 상태로 되돌아옴


lbl("frame_name",root,f12,BLACK,'그룹웨어 자동결제',0,1,5,5)
lbl("id_name",root,f10,BLACK,'ID',1,0,5,5)
lbl("pw_name",root,f10,BLACK,'PW',2,0,5,5)

entry_1 = Entry(root, width=5) # ID 입력
entry_1.insert(END, '')
entry_1.grid(row=1,column=1,padx=5, pady=5, sticky=N+E+W+S)
 
entry_2 = Entry(root, width=5,show='*') # PW 입력 / show='*'은 별로 표시한다는 것
entry_2.insert(END, '')
entry_2.grid(row=2,column=1,padx=5, pady=5, sticky=N+E+W+S)

btn = Button(root,font=f12,fg=IDIS_COLOR,text='Enter',command=btn_cmd)
btn.grid(row=1,rowspan=2,column=3,padx=5,pady=5,sticky=N+E+W+S)

btn.bind("<Button-1>",btn_cmd) # 마우스 왼쪽클릭 누르면 실행된다
btn.bind('<Return>',btn_cmd) # 엔터키를 누르면 실행된다

root.mainloop() #Tkinter를 여기서 끝낸다


