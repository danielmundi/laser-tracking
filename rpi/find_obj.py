import io
import socket
import struct
import time
import picamera
import picamera.array
import cv2
import numpy as np

client_socket = socket.socket()
client_socket.connect(('10.42.0.1', 8000))

height = 240
width = 320
#height = 480
#width = 640

# Accept a single connection and make a file-like object out of it
connection = client_socket.makefile('wb')
try:
    #connection.write(struct.pack("<LLL", height, width, 3))
    client_socket.sendall(struct.pack("<LLL", height, width, 1))

    with picamera.PiCamera() as camera:
        camera.resolution = (width, height)
        camera.framerate = 10
        rawCapture = picamera.array.PiRGBArray(camera, size=(width, height))
        # Start a preview and let the camera warm up
        #camera.start_preview()
        time.sleep(0.1)

        #start = time.time()
        #conn_write = connection.write

        # Indentify color red
        lower = np.array([3, 165, 110], dtype = "uint8")
        upper = np.array([12, 255, 255], dtype = "uint8")
        kernel = np.ones((5,5),np.uint8)

        print("Sending images")

        for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
            # Grab the raw NumPy array representing the image
            image = frame.array
            #print("size: {0}".format(image.size))

            blurred = cv2.GaussianBlur(image, (5, 5), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower, upper)
            #output = cv2.bitwise_and(image, image, mask=mask)

            #thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

            #opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            #closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

            client_socket.sendall(closing.data)
            #connection.flush()

            #print("Image sent")

            #finish = time.time()
            #print("%.1f FPS" % float(1/(finish-start)))
            #start = finish

            rawCapture.truncate(0)
except (KeyboardInterrupt):
    pass
finally:
    #connection.close()
    client_socket.close()
