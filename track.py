#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pigpio
import time
import cv2
import numpy as np

pi = pigpio.pi()

X_MAX = 1700 #→
X_MIN = 900 #←
X_HOME = 1300
Y_MAX =  1500#下
Y_MIN =  800#上
Y_HOME = 900 

capture = cv2.VideoCapture(0)
capture.set(3, 240)
capture.set(4, 160)
width = capture.get(3)
height = capture.get(4)



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
    while True:
        _, img = capture.read()
        dst = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        conditions = (dst[:,:,0]<150)*1 * ((dst[:,:,0]>90)*1) * (dst[:,:,1]>100)

        sum_item = np.sum(conditions)
        t_conditions = np.transpose(conditions)

        temp = range(len(conditions))
        mean_y = int(np.sum([temp * t_condition for t_condition in t_conditions])/sum_item)
        temp = range(len(t_conditions))
        mean_x = int(np.sum([temp * condition for condition in conditions])/sum_item)

        #cv2.circle(img, (mean_x, mean_y),10, (0,0,255), -1)  
        # cv2.imshow("camera", img)

        move_degree_x = now_degree_x  - (mean_x-width/2)*0.2 #240/2
        move_degree_y = now_degree_y + (mean_y-height/2)*0.2 #160/2
        #print("{},{},{},{},{},{}".format(mean_x,mean_y,(mean_x-width/2),(mean_y-height/2), width, height))
        move(move_degree_x, move_degree_y)
        now_degree_x = move_degree_x
        now_degree_y = move_degree_y
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    
    capture.release()
    cv2.destroyAllWindows()



    


if __name__ == '__main__':
    main()