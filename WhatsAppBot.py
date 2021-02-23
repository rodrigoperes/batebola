#from selenium import webdriver

#browser = webdriver.Firefox()

import time
import numpy as np
import cv2
import statistics
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message

def countPeople():
    # initialize the HOG descriptor/person detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    
    # open webcam video stream
    cap = cv2.VideoCapture(0)
    boxes_arr = np.array([])

    while len(boxes_arr) < 21:

        # Capture frame-by-frame
        (ret, frame) = cap.read()

        # resizing for faster detection
        frame = cv2.resize(frame, (640, 480))
        # using a greyscale picture, also for faster detection
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # detect people in the image
        # returns the bounding boxes for the detected objects
        boxes, weights = hog.detectMultiScale(frame, winStride=(8,8))
        
        print(len(boxes))
        boxes_arr = np.append(boxes_arr, len(boxes))
        
    # When everything done, release the capture
    cap.release()
    # finally, close the window
    cv2.destroyAllWindows()
    
    mode = int(statistics.mode(boxes_arr))
    
    return mode
    

driver = WhatsAPIDriver()
print("Waiting for QR")
time.sleep(30)

print("Bot started") 
#print(driver.get_all_chat_ids()) 

while True:
    time.sleep(3)
    #print("Checking for more messages")
    try:
        for contact in driver.get_unread(include_me=True):
            for message in contact.messages:
                if isinstance(message, Message): # Currently works for text messages only.
                    if message.content == '#BATEBOLA':
                        qtd = countPeople()
                        
                        if qtd == 0:
                            response = 'Fiteye informa: ninguém batendo bola no momento!'
                        else:
                            response = 'Fiteye informa: há '+ str(qtd) +' pessoa(s) batendo bola neste momento!'
                            
                        contact.chat.send_message(response)
    except:
        continue