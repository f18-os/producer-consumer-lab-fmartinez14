#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue
from threading import Thread
from threading import Timer
from threading import Lock
import time

leQuequeDeParis= queue.Queue(10)
DisplayQueque = queue.Queue(10)

def extractFrames(fileName):
    # Initialize frame count 
    count = 0

    # open video file
    vidcap = cv2.VideoCapture(fileName)

    # read first image
    success,image = vidcap.read()
    
    print("Reading frame {} {} ".format(count, success))
    while success:
        # get a jpg encoded frame
        success, jpgImage = cv2.imencode('.jpg', image)

        #encode the frame as base 64 to make debugging easier
        jpgAsText = base64.b64encode(jpgImage)

        if count == 100:
        	break
        # add the frame to the buffer
        leQuequeDeParis.put(jpgAsText)
       
        success,image = vidcap.read()
        print('Reading frame {} {}'.format(count, success))
        count += 1
    leQuequeDeParis.put("Done")
    print("Frame extraction complete")

def grayScaleImages():

    count = 0 

    startSize = leQuequeDeParis.qsize()

    while True:
        print("Converting frame {}".format(count))

        frameAsText = leQuequeDeParis.get(True)
        if frameAsText == "Done":
        	DisplayQueque.put("Done")
        	break;
        # decode the frame 
        jpgRawImage = base64.b64decode(frameAsText)

        # convert the raw frame to a numpy array
        jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)
        
        # get a jpg encoded frame
        img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)

        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)



        returnValue, imageValue = cv2.imencode('.jpg',grayscaleFrame)
        #encode the frame as base 64 to make debugging easier
        saveToBuffer = base64.b64encode(imageValue)


        # useMe = np.fromstring(base64.b64decode(leText), dtype=np.uint8)
        # showImage = cv2.imdecode(useMe, cv2.IMREAD_COLOR)


        # add the frame to the buffer
        DisplayQueque.put(saveToBuffer)

        count += 1
    print("finished converting frames")

def displayFrames():
    # initialize frame count
    count = 0
    # go through each frame in the buffer until the buffer is empty
    while True:
        # get the next frame
        frameAsText =  DisplayQueque.get(True)

        if frameAsText == "Done":
        	break;

        # decode the frame 
        jpgRawImage = base64.b64decode(frameAsText)


        useMe = np.fromstring(jpgRawImage, dtype=np.uint8)

        img = cv2.imdecode(useMe, cv2.IMREAD_COLOR)


        print("Displaying frame {}".format(count))        

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow("Video", img)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1
        # time.sleep(1)

    print("Finished displaying all frames")
    # cleanup the windows
    cv2.destroyAllWindows()

def getThreads():
	print("starting le threads")

	#les arguments
	leFileName = "clip.mp4"
    #l' finale de arguments

    #le Threads
	extractThread = Thread(target=extractFrames,args=[leFileName])
	grayThread = Thread(target=grayScaleImages)
	displayThread = Thread(target=displayFrames)
	extractThread.start()
	grayThread.start()
	displayThread.start()
	# timer1 = Timer(1.0,grayThread.start)
	# timer2= Timer(2.0,displayThread.start)
	# timer1.start()
	# timer2.start()
	# extractThread.start()

print("Starting up")


getThreads()
# leFileName = "clip.mp4"

# leQuequeDeParis= queue.Queue()

# extractFrames(leFileName,leQuequeDeParis)
# grayScaleImages(leQuequeDeParis)
# displayFrames(leQuequeDeParis) 






