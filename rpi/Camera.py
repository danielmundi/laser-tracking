import io
import socket
import struct
import time
import picamera
import picamera.array
import cv2
import numpy as np
from threading import Thread
import threading
from Identification import Identification

class Camera(Thread):
    def __init__(self, sampling_period):
        Thread.__init__(self)
        self.connect = True

        self.height = 240
        self.width = 320

        self.object = Identification()
        self.laser = Identification()

        self.sampling_period = sampling_period

        if self.connect:
            self.connect_server('10.42.0.1', 8001)

        self.__stop = threading.Event()

    def run(self):
        self.start_indentifying()

    def connect_server(self, ip, port):
        self.sock = socket.socket()
        self.sock.connect((ip, port))
        #sock.connect(('192.168.1.152', 8000))

        # Send the size of the images
        self.sock.sendall(struct.pack("<LLL", self.height, self.width, 3))

    def start_indentifying(self):
        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (self.width, self.height)
                camera.framerate = 1/self.sampling_period
                camera.awb_mode = "sunlight"
                rawCapture = picamera.array.PiRGBArray(camera, size=(self.width, self.height))
                # Start a preview and let the camera warm up
                time.sleep(0.1)

                # Identify blue sponge
                lower_obj = np.array([100, 0, 0], dtype = "uint8")
                upper_obj = np.array([120, 255, 255], dtype = "uint8")

                # Indentify laser
                lower_laser = np.array([19, 0, 255], dtype = "uint8")
                upper_laser = np.array([255, 255, 255], dtype = "uint8")

                kernel = np.ones((5,5),np.uint8)

                center_x_obj_norm = center_y_obj_norm = center_x_laser_norm = center_y_laser_norm = 0

                print("Sending images")

                for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
                    # Grab the raw NumPy array representing the image
                    image = frame.array
                    #print("size: {0}".format(image.size))

                    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

                    blurred = cv2.GaussianBlur(hsv, (5, 5), 0)

                    mask_obj = cv2.inRange(blurred, lower_obj, upper_obj)
                    mask_laser = cv2.inRange(hsv, lower_laser, upper_laser)
                    #output = cv2.bitwise_and(image, image, mask=mask)

                    mask_obj = cv2.erode(mask_obj, None, iterations=2)
                    mask_obj = cv2.dilate(mask_obj, None, iterations=2)
                    #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                    #closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

                    cnts_obj = cv2.findContours(mask_obj, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
                    cnts_laser = cv2.findContours(mask_laser, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

                    if len(cnts_obj) > 0:
                        c_obj = max(cnts_obj, key=cv2.contourArea)

                        rect = cv2.minAreaRect(c_obj)
                        center_x_obj, center_y_obj = rect[0] #rect = ((center_x,center_y),(width,height),angle)
                        center_x_obj, center_y_obj = int(center_x_obj), int(center_y_obj)
                        box = cv2.boxPoints(rect)
                        box = np.int0(box)
                        cv2.drawContours(image, [box], 0, (0,255,0), 2)
                        cv2.circle(image, (center_x_obj, center_y_obj), 3, (255,255,255), -1)

                        center_x_obj_norm = center_x_obj/self.width-1/2
                        center_y_obj_norm = -center_y_obj/self.height+1/2

                        self.object.visible = True
                        self.object.position = (center_x_obj_norm, center_y_obj_norm)
                    else:
                        self.object.visible = False

                    if len(cnts_laser) > 0:
                        c_laser = max(cnts_laser, key=cv2.contourArea)

                        (x, y), radius = cv2.minEnclosingCircle(c_laser)
                        (center_x_laser, center_y_laser) = (int(x), int(y))
                        radius = int(radius)
                        cv2.circle(image, (center_x_laser, center_y_laser), radius+5, (255,0,0), -1)

                        center_x_laser_norm = center_x_laser/self.width-1/2
                        center_y_laser_norm = -center_y_laser/self.height+1/2

                        self.laser.visible = True
                        self.laser.position = (center_x_laser_norm, center_y_laser_norm)
                    else:
                        self.laser.visible = False

                    print("obj=({0},{1})\t laser=({2},{3})".format(center_x_obj_norm, center_y_obj_norm, center_x_laser_norm, center_y_laser_norm))

                    if self.connect:
                        self.sock.sendall(image.data)

                    rawCapture.truncate(0)

                    if self.stopped():
                        break
        except (KeyboardInterrupt):
            pass
        finally:
            if self.connect:
                self.sock.close()

    def stop(self):
        self.__stop.set()

    def stopped(self):
        return self.__stop.isSet()