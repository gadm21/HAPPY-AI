"""
Reads a frame from RTSP feed and saves the frame if it contains a car.
Darkflow is used to detect car objects.
"""

import os
from darkflow.net.build import TFNet
from os import listdir
from os.path import isfile, join
import numpy
import cv2
import time
import datetime
from os.path import isfile, join
import common

vidcap = cv2.VideoCapture(common.RTSP_FEED)
options = {"model": common.CFG_PATH, "load": common.YOLO_WEIGHTS_PATH, "threshold": 0.25}
timestr = time.time() # Gets time in seconds since 1971.
tfnet = TFNet(options)
fps = 12
count = 0

while True:
    status, frame = vidcap.read()
    print("Read new frame {}".format(count))
    
    if count%int(fps/2) == 0:
        try:
            result = tfnet.return_predict(frame)
            hasCar = False
            for r in result:
                if (r['label']) == 'car':
                    hasCar = True
                    break
            if hasCar:
                print("-> Found car")
                cv2.imwrite(os.path.join(common.CARS_PATH, 'frame%d.jpg' %timestr), frame)
        except Exception as e:
            print(e)
    count += 1
    timestr += 1
