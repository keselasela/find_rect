import cv2
import numpy as np
from operator import itemgetter
mean_x,mean_y = -1,-1
width = 240
height = 160
th_area = width*height / 100 #34800/100
if __name__ == "__main__":
  
  
  capture = cv2.VideoCapture(0)
  capture.set(3, width)
  capture.set(4, height)
  n=0
  def search_point():
    
  while cv2.waitKey(30) < 0:

    _, frame = capture.read()
    #approx= find_aporox_of_rect(frame)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:,:,2]
    mask = np.zeros(h.shape, dtype=np.uint8)
    mask[((h < 20) | (h > 200)) & (s > 70) & (v>150)] = 255
    img, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    approxes = []
    areas = []
    for contour in contours:
      

      arclen = cv2.arcLength(contour, True)
      approx = cv2.approxPolyDP(contour, 0.05*arclen, True)
      if len(approx) != 4 or cv2.contourArea(contour) < 50:
        #
        continue
      approxes.append(approx)
      area = cv2.contourArea(contour)
      areas.append(area)

    if len(approxes)>0:
      
      
      target_rect = sorted(zip(approxes,areas),reverse=True,key=itemgetter(1))
      n = n+1
      print("{}:{}".format(n,target_rect))
      print("---------------------------------------------")
    else:
      target_rect = []
    
    #if len(target_rect)>0:
      #print("---------------------------------------------")
      #print(target_rect[0])
      #
      #point = np.sum(target_rect[0], axis=0)[0]
      #mean_x = point[0]/4
      #mean_y = point[1]/4
      #print(mean_x,mean_y)
      #print(target_rect[1])
    mean_x, mean_y = -1,-1
    
    
    cv2.imshow('red', frame)
    cv2.imshow('aaa', mask)
  capture.release()
  cv2.destroyAllWindows()