#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import queue




def extractFrames(fileName, outputBuffer):
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
        outputBuffer.put(jpgAsText)
       
        success,image = vidcap.read()
        print('Reading frame {} {}'.format(count, success))
        count += 1

    print("Frame extraction complete")

def grayScaleImages(inputBuffer):

    count = 0 

    startSize = inputBuffer.qsize()
    while count < startSize:
        print("Converting frame {}".format(count))

        frameAsText = inputBuffer.get()

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
        inputBuffer.put(saveToBuffer)

        count += 1


def displayFrames(inputBuffer):
    # initialize frame count
    count = 0
    # go through each frame in the buffer until the buffer is empty
    while not inputBuffer.empty():
        # get the next frame
        frameAsText = inputBuffer.get()
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

    print("Finished displaying all frames")
    # cleanup the windows
    cv2.destroyAllWindows()


    

print("Starting up")

leFileName = "clip.mp4"

leQuequeDeParis= queue.Queue()

extractFrames(leFileName,leQuequeDeParis)
grayScaleImages(leQuequeDeParis)
displayFrames(leQuequeDeParis) 






