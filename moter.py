#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import serial
import time
import threading
import pigpio
pi = pigpio.pi()
ser = serial.Serial('/dev/ttyUSB0',115200,timeout=None)
flag = True

def move(degree_x, degree_y):  
  pi.set_servo_pulsewidth(4, degree_x)
  pi.set_servo_pulsewidth(17, degree_y)
def moter():
	while(flag):
		#straight = (100,96)
		#run(100,70) #→
		run(95,100) #←
		#run(100,95)
		
		time.sleep(1)
		run(0,0)
		time.sleep(1)



def run(left, right):
	text_left = 'm1:{}\n'.format(-left)
	text_right = 'm0:{}\n'.format(-right)
	ser.write(str.encode(text_left))
	ser.write(str.encode(text_right))

def main():
	th = threading.Thread(target=moter)
	th.setDaemon(True)
	th.start()

	global flag
	input()
	flag = False
	move(1300,1300)
	ser.write(str.encode('m0:0\n'))
	ser.write(str.encode('m1:0\n'))
	ser.close() 

if __name__ == "__main__":
    print("start")
    main()


