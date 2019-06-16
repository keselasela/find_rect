import cv2
import numpy as np
from operator import itemgetter
import time
import math
import threading
import pigpio
import serial
flag = True
ser = serial.Serial('/dev/ttyUSB0',115200,timeout=None)
#ser = serial.Serial('/dev/ttyUSB0',115200,timeout=None)

pi = pigpio.pi()
X_MAX = 1700 #→
X_MIN = 900 #←
X_HOME = 1300
Y_MAX =  1500#下
Y_MIN =  800#上
Y_HOME = 1300

now_degree_x, now_degree_y = X_HOME,Y_HOME
mean_x,mean_y = -1,-1
width,height = 420,160
th_area = width*height / 100 #34800/100
mask =np.zeros(width*height, dtype=np.uint8)

def main():
  global mask
  global width,height
  capture = cv2.VideoCapture(0)
  capture.set(3, width)
  capture.set(4, height)
  t1 = threading.Thread(target=search_point)
  t1.setDaemon(True)
  t1.start()
  #t2 = threading.Thread(target=approach)
  #t2.setDaemon(True)
  #t2.start()
  width,height = capture.get(3),capture.get(4)
  #t2 = threading.Thread(target=track)
  #t2.setDaemon(True)
  #t2.start()
    
  while (True):

    _, frame = capture.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:,:,2]
    
    mask = np.zeros(h.shape, dtype=np.uint8)
    mask[((h < 20) | (h > 200)) & (s > 70) & (v>150)] = 255
    cv2.imshow('red', frame)
    cv2.imshow('mask', mask)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
       break
  capture.release()
  cv2.destroyAllWindows()

def run(left, right):
 
  text_left = 'm1:{}\n'.format(-left)
  text_right = 'm0:{}\n'.format(-right)
  ser.write(str.encode(text_left))
  ser.write(str.encode(text_right))

def approach():
  while(1):
    if not flag and not(mean_x == -1 or mean_y==-1):
      if now_degree_x - 1300 <-30:
        run(100,70)
        print("→→")
      elif now_degree_x - 1300 >30:
        run(95,100) 
        print("←←")
      else:
        run(100,95)
        print("真っ直ぐ")
      #time.sleep(1)
    elif not flag and (mean_x == -1 or mean_y==-1) :
      run(0,0)
  

def move(degree_x, degree_y):  
  pi.set_servo_pulsewidth(4, degree_x)
  pi.set_servo_pulsewidth(17, degree_y)
#
def searching(n):
  global now_degree_x,now_degree_y
  global flag
  
  if mean_x != -1 and mean_y != -1:
    print("ssssssssssssssssss")
    flag = False

  if flag :
    if n%7==0:
      now_degree_x, now_degree_y = 1300,1300

    elif n%7==1:
      now_degree_x, now_degree_y = 1000,1300

    elif n%7==2:
      now_degree_x, now_degree_y = 1000,1000

    elif n%7==3:
      now_degree_x, now_degree_y = 1300,1000
    elif n%7==4:
      now_degree_x, now_degree_y = 1600,1000
    elif n%7==5:
      now_degree_x, now_degree_y = 1600,1300
    
    

  
  time.sleep(3)
  move(now_degree_x, now_degree_y)
  
def search_point():
  global now_degree_x,now_degree_y
  n=0
  global mean_x,mean_y
  now_degree_x, now_degree_y, move_degree_x, move_degree_y = X_HOME,Y_HOME,0,0
  move(X_HOME,Y_HOME)
  while(True):
    n = n+1
    if flag:
      searching(n)
    
    img, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    approxes = []
    areas = []
    for contour in contours:

      arclen = cv2.arcLength(contour, True)
      approx = cv2.approxPolyDP(contour, 0.05*arclen, True)
      if len(approx) != 4 or cv2.contourArea(contour) < 50 or cv2.contourArea(contour) >5000:
        
        continue
      approxes.append(approx)
      area = cv2.contourArea(contour)
      areas.append(area)

    if len(approxes)>0:

      target_rect = sorted(zip(approxes,areas),reverse=True,key=itemgetter(1))[0]
      print(target_rect[1])
      point = np.sum(target_rect[0], axis=0)[0]
  
      mean_x = point[0]/4
      mean_y = point[1]/4
      
    else:
      mean_x, mean_y = -1,-1
    #print(mean_x,mean_y)

    if(mean_x == -1 or mean_y==-1) or ((abs(mean_y-height/2)<10 and abs(mean_x-width/2)<10)):
      continue
    
    move_degree_x = now_degree_x  - (mean_x-width/2)*0.03 #240/2
    move_degree_y = now_degree_y + (mean_y-height/2)*0.03 #160/2
    

    move(move_degree_x, move_degree_y)
    now_degree_x = move_degree_x
    now_degree_y = move_degree_y
    



if __name__ == "__main__":
    main()