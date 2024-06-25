import cv2
import random
vidcap = cv2.VideoCapture('video3.mkv')
i = 1
def getFrame(sec, i):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        
        cv2.imwrite("folder/"+str(i)+" frame.png", image)     # save frame as PNG file
    return hasFrames
sec = 0
frameRate = 4 #it will capture image in each 0.25 second
success = getFrame(sec, i)
while success:
    sec = sec + frameRate
    sec = round(sec, 2)
    print('Frame ' + i+1)
    i = i + 1
    success = getFrame(sec, i)