import sys
import io
import socket
import cv2
import struct
import numpy as np

# Start a socket to listen for connections on 0.0.0.0:8000
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

while True:
    try:
        print("Waiting for connection...")
        #connection = server_socket.accept()[0].makefile('rb')
        sock, addr = server_socket.accept()

        #image_sizes = struct.unpack('<LLL', connection.read(struct.calcsize('<LLL')))
        image_sizes = struct.unpack('<LLL', sock.recv(struct.calcsize('<LLL')))
        height = image_sizes[0]
        width = image_sizes[1]
        depth = image_sizes[2]

        image_size = height*width*depth

        image_default = np.zeros((height, width, depth), np.uint8)
        image = image_default.copy()

        #image.data = connection.read(image_size)
        #connection.read(image_size)
        image.data = sock.recv(image_size, socket.MSG_WAITALL)
        while True: #image.data:
            #sys.stdout.write("Image received")

            cv2.imshow("Image", image)
            cv2.waitKey(1)

            image = image_default.copy()
            #image.data = connection.read(image_size)
            #connection.read(image_size)
            image.data = sock.recv(image_size, socket.MSG_WAITALL)

    except (KeyboardInterrupt):
        break
    #except(Exception):
        #pass
    finally:
        cv2.destroyWindow("Image")
        #connection.close()
        sock.close()

server_socket.close()
