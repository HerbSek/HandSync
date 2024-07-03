import cv2
# import numpy as np 
# # import pyautogui
# import time 
 

# time.sleep(5)
# cam = cv2.VideoCapture(0)
# width, height = pyautogui.size()
# cascade_face = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

# if not cam.isOpened():
#     raise IOError('Camera not detected')
 
# while True:
#     ret, frame = cam.read()

#     if not ret:
#         break
   
#     frame = cv2.resize(frame, (int(width),int(height)) , interpolation= cv2.INTER_AREA)
#     frame = cv2.flip(frame,1)
#     grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    

#     load_cascade = cascade_face.detectMultiScale(grey, 1.2, 3) 
#     for (x,y,w,h) in load_cascade:
#         cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2) 
        
#         center_x = x + w // 2
#         center_y = y + h // 2

#         pyautogui.moveTo(center_x,center_y) 
        
#         print(f"Center coordinates: ({int(0.5*(w))}, {int(0.5*(h))})")

#     # cv2.imshow('frame', frame)
#     c = cv2.waitKey(100)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cam.release()
# cv2.destroyAllWindows()  


print([x for x in dir(cv2) if x.startswith('COLOR_BGR2')])