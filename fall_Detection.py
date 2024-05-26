#Based on Zed code - Person Fall detection using raspberry pi camera and opencv lib. Link: https://www.youtube.com/watch?v=eXMYZedp0Uo

import cv2
import time
import serial
import os, time
port = serial.Serial("COM3", baudrate=9600, timeout=1)
fitToEllipse = False
cap = cv2.VideoCapture('queda.mp4')
time.sleep(2)

fgbg = cv2.createBackgroundSubtractorMOG2()
j = 0

while(1):
    ret, frame = cap.read()
    
    #Convert each frame to gray scale and subtract the background
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fgmask = fgbg.apply(gray)
        
        #Find contours
        contours, _ = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
        
            # List to hold all areas
            areas = []

            for contour in contours:
                ar = cv2.contourArea(contour)
                areas.append(ar)
            
            max_area = max(areas, default = 0)

            max_area_index = areas.index(max_area)

            cnt = contours[max_area_index]

            M = cv2.moments(cnt)
            
            x, y, w, h = cv2.boundingRect(cnt)

            cv2.drawContours(fgmask, [cnt], 0, (255,255,255), 3, maxLevel = 0)
            
            if h < w:
                j += 1
                
            if j > 10:
                print("FALL")
                print (j)
                cv2.putText(fgmask, 'FALL', (x, y), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 2)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
                port.write(b'A\r')
                rcv = port.read(10)
                print(rcv)
                time.sleep(1)
                port.write(b"AT+CMGF=1\r")
                print("text Mode Enabled…")
                time.sleep(3)
                port.write(b'AT+CMGS="7499221456"\r')
                msg = "fall detected need help"
                print("sending message….")
                time.sleep(3)
                port.reset_output_buffer()
                time.sleep(1)
                port.write(str.encode(msg+chr(26)))
                time.sleep(30)
            if j > 24:
                print("sleep")
                print (j)
                cv2.putText(fgmask, 'Sleep', (x, y), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 2)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)   

            if h > w:
                j = 0 
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)


            cv2.imshow('video', frame)
        
            if cv2.waitKey(33) == 27:
             break
    except Exception as e:
        break
cv2.destroyAllnmmn,mWindows()
