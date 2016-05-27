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
#client_socket.connect(('192.168.1.152', 8000))

height = 240
width = 320
#height = 480
#width = 640

# Accept a single connection and make a file-like object out of it
connection = client_socket.makefile('wb')
try:
    #connection.write(struct.pack("<LLL", height, width, 3))
    client_socket.sendall(struct.pack("<LLL", height, width, 3))

    with picamera.PiCamera() as camera:
        camera.resolution = (width, height)
        camera.framerate = 10
        camera.awb_mode = "sunlight"
        rawCapture = picamera.array.PiRGBArray(camera, size=(width, height))
        # Start a preview and let the camera warm up
        #camera.start_preview()
        time.sleep(0.1)

        #start = time.time()
        #conn_write = connection.write

        # Indentify color red
        #lower = np.array([3, 150, 90], dtype = "uint8")
        #upper = np.array([12, 255, 255], dtype = "uint8")

        # Identify blue sponge
        lower_obj = np.array([100, 0, 0], dtype = "uint8")
        upper_obj = np.array([120, 255, 255], dtype = "uint8")

        # Indentify laser
        lower_laser = np.array([19, 0, 255], dtype = "uint8")
        upper_laser = np.array([255, 255, 255], dtype = "uint8")

        kernel = np.ones((5,5),np.uint8)

        center_x_obj = center_y_obj = center_x_laser = center_y_laser = 0

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

            if len(cnts_laser) > 0:
                c_laser = max(cnts_laser, key=cv2.contourArea)

                (x, y), radius = cv2.minEnclosingCircle(c_laser)
                (center_x_laser, center_y_laser) = (int(x), int(y))
                radius = int(radius)
                cv2.circle(image, (center_x_laser, center_y_laser), radius+5, (255,0,0), -1)

            print("obj=({0},{1})\t laser=({2},{3})".format(center_x_obj, center_y_obj, center_x_laser, center_y_laser))

            client_socket.sendall(image.data)
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
