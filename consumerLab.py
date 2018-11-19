#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue
from threading import Thread
from customQueue import Q

# grayScaleQueue= queue.Queue(10)    #Old queues used by previous version using Queue.queue.
# DisplayQueque = queue.Queue(10)

grayScaleQueue = Q(10)
DisplayQueque = Q(10)

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

        # add the frame to the buffer
        grayScaleQueue.put(jpgAsText)
       
        success,image = vidcap.read()
        print('Reading frame {} {}'.format(count, success))
        count += 1
    grayScaleQueue.put("Done")
    print("Frame extraction complete")

def grayScaleImages():

    count = 0 

    while True:

        frameAsText = grayScaleQueue.get()
        if frameAsText == "Done":
        	DisplayQueque.put("Done")
        	break;

        print("Converting frame {}".format(count))

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
        frameAsText =  DisplayQueque.get()

        if frameAsText == "Done":
        	break;

        # decode the frame 
        jpgRawImage = base64.b64decode(frameAsText)

        #Using a from string to load the already existing numpy array sent by the grayscale thread.
        useMe = np.fromstring(jpgRawImage, dtype=np.uint8)

        #Decode Image
        img = cv2.imdecode(useMe, cv2.IMREAD_COLOR)


        print("Displaying frame {}".format(count))        

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow("Video", img)
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        count += 1


    print("Finished displaying all frames")
    # cleanup the windows
    cv2.destroyAllWindows()

def getThreads():
	print("starting Threads")

	#Video file name
	leFileName = "clip.mp4"

    #Creation of all three threads.
	extractThread = Thread(target=extractFrames,args=[leFileName])
	grayThread = Thread(target=grayScaleImages)
	displayThread = Thread(target=displayFrames)

	#Starting threads.
	extractThread.start()
	grayThread.start()
	displayThread.start()


print("Starting up")


getThreads()






