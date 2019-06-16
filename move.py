#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pigpio
import time
import cv2
import numpy as np
import threading

pi = pigpio.pi()

X_MAX = 1700 #→
X_MIN = 900 #←
X_HOME = 1300
Y_MAX =  1500#下
Y_MIN =  800#上
Y_HOME = 900 

#capture = cv2.VideoCapture(0)
#capture.set(3, 360)
#capture.set(4, 240)
#width = capture.get(3)
#height = capture.get(4)



#　左　←　0　→　右
#  上　←　0　→　下
#def move(degree_x, degree_y):
#    duty_x = int(-degree_x + X_HOME)
#    duty_y = int(degree_y + Y_HOME)   
#    pi.set_servo_pulsewidth(4, duty_x)
#    pi.set_servo_pulsewidth(17, duty_y)
def move(degree_x, degree_y):  
    pi.set_servo_pulsewidth(4, degree_x)
    pi.set_servo_pulsewidth(17, degree_y)

def main():
    now_degree_x, now_degree_y, move_degree_x, move_degree_y = X_HOME,Y_HOME,0,0
    move(X_HOME,Y_HOME)
    th = threading.Thread(target=track)
    th.setDaemon(True)
    th.start()
    while True:
        ret, frame = capture.read()
 
        cv2.imshow('Capture',frame)
        
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    
    capture.release()
    cv2.destroyAllWindows()

def track():
    print(111)
    while():
        left,right = input().split(" ")
        print(left,right)
        move(left,right)


if __name__ == '__main__':
    main()