import numpy as np
from PIL import ImageGrab
import cv2
import time
import math
# import pyautogui
#from directkeys import *
from lib.getkeys import key_check
# import os
# from alexnet import alexnet
import sqlite3
WIDTH=28
HEIGHT=28
LR= 1e-3
EPOCH=8
MODEL_NAME= 'MarioAI-{}-{}-{}-epochs.model'.format(LR,'alexnetv2',EPOCH)
conn= sqlite3.connect('DQN.db',detect_types=sqlite3.PARSE_DECLTYPES,isolation_level=None)
cur= conn.cursor()
cur.execute("PRAGMA synchronous = OFF;")
cur.execute("PRAGMA journal_mode=WAL;")
cur.execute("PRAGMA read_uncommitted = true;")
Gather=False
def KeyPressButtons(key):
    
    if(key==0):
        ReleaseKey(X)
        PressKey(Z)
    elif(key==2):
       # print("here")
        PressKey(X)
        PressKey(Z)
    else:
        ReleaseKey(X)
        ReleaseKey(Z)

def KeyPressArrows(key):
    
    if(key==0):
        ReleaseKey(X)
        PressKey(Z)
    elif(key==2):
       # print("here")
        PressKey(X)
        PressKey(Z)
    else:
        ReleaseKey(X)
        ReleaseKey(Z)                     
# pyautogui.typewrite(['down','enter'])
# for i in list(range(4))[::-1]:
#     print(i+1)
#     time.sleep(1)
# pyautogui.typewrite(['down','enter'])

# model =alexnet(WIDTH,HEIGHT,LR)
# model.load(MODEL_NAME)

#model2=alexnet(WIDTH,HEIGHT,LR)
#model2.load(MODEL_NAME2)




def process_img(original_image):
    processed_img=cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img= cv2.resize(processed_img,(28,28))
    #rocess_img=cv2.Canny(processed_img, threshold1=200, threshold2=300)
    return processed_img

def reset():
    pyautogui.moveTo(8,50,duration=.25)
    pyautogui.click(8,50)
    pyautogui.moveTo(8, 200, duration=0.25)
    pyautogui.click(8,200)
    pyautogui.moveTo(220, 200, duration=0.25)
    pyautogui.click(220,180)

def pause():
    pyautogui.click(70,50)
    pyautogui.moveTo(70,75, duration=0.25)
    pyautogui.click(70,75)    

def determine_key(time_step):
    if 0<=time_step<30:
        return RIGHT
    elif 30<=time_step:
        return X


def screen_record(): 
    '''
    OpenCV Prototype Unused
    '''
    last_time = time.time()
    time_step=0
    paused=False
    while(True):
        if not paused:
            # 800x600 windowed mode
            #PressKey(determine_key(time_step))
            printscreen =  np.array(ImageGrab.grab(bbox=(0,60,580,530)))
            new_screen=process_img(printscreen)
            #print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()

            prediction=model.predict([new_screen.reshape(WIDTH,HEIGHT,1)])[0]
            #prediction2=model.predict2([new_screen.reshape(WIDTH,HEIGHT,1)])[0]
            moves=list(np.around(prediction))
            #moves2=list(np.around(prediction2))
            print(moves,prediction)
            if moves==[1,0,0,0]:
                KeyPressButtons(0)
            elif moves==[0,0,1,0]:
                KeyPressButtons(2)    
            else:
                KeyPressButtons(3)   
            time.sleep(1.0)
            ReleaseKey(X)
            #cv2.imshow('window2',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
            #v2.imshow('window',new_screen)k     
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break         
            #ReleaseKey(determine_key(time_step))    
            time_step+=1  
        keys=key_check()
        #print(keys)
        if 'P' in keys:
            paused=(1-int(paused))
            time.sleep(1)
            KeyPressButtons(3)
            pause()

        if 'Q' in keys:
            cv2.destroyAllWindows()
            break

def update_table(image,action):  
    sql = ''' UPDATE rewards
              SET 
              image=?,
              action=?,
              done=1
              WHERE image is NULL'''
    cur.execute(sql, (image,action))
    conn.commit()
def check_table():
    sql = "Select done from rewards where done <> 1"
    cur.execute(sql)
    row=cur.fetchone()
    if row==None:
        return WAIT  
    current=row[0]
    return current

frame_count=0
ACTION,WAIT,DEATH=0,1,2
while check_table()==WAIT:
    pass
print("Ready!")    
while True:
    keys=key_check()
    check=check_table()
    if 'Q' in keys:
        break
    if check==ACTION: #Mario Needs an Action
        print_screen = np.array(ImageGrab.grab(bbox=(0,60,580,530)))
        new_screen=process_img(print_screen)
        button=8
        print("update "+str(frame_count))
        update_table(new_screen,button)    
        print("update completed")
        frame_count+=1
    elif check==DEATH: #Mario has Died
        print("DEATH")
        break 
cur.close()
conn.close()
#reset()
#pause()
#screen_record()
#pause()


