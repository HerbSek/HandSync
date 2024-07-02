import cv2
import numpy as np 
import pyautogui

cam = cv2.VideoCapture(0)
width, height = pyautogui.size()
cascade_face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

if not cam.isOpened():
    raise IOError('Camera not detected')

while True:
    ret, frame = cam.read()

    if not ret:
        break
   
    frame = cv2.resize(frame, (int(width),int(height)) , interpolation= cv2.INTER_AREA)
    frame = cv2.flip(frame,1)
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    

    load_cascade = cascade_face.detectMultiScale(grey, 1.4, 5) 
    for (w,h,i,j) in load_cascade:
        cv2.rectangle(frame, (w,h), (w+i,h+j), (255,0,0), 2) 
        center_x = w + i // 2
        center_y = h + j // 2
        
        pyautogui.moveTo(center_x,center_y) 
        
        print(f"Center coordinates: ({center_x}, {center_y})")

    # cv2.imshow('frame', frame)
    c = cv2.waitKey(10)
    if c == ord(' '):
        break
cam.release()
cv2.destroyAllWindows()


