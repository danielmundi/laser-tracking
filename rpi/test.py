import pigpio, time, io
from Motor import Motor
from Controller import Controller
from Camera import Camera
import threading
from Identification import Identification

def main():
    global x, y, run
    x = y = 0
    run = True

    pi = pigpio.pi()

    motorx = Motor(pi,1)
    motory = Motor(pi,2)

    sampling_period = 0.2

    control = Controller(pi, motorx, motory, sampling_period)

    camera = Camera(sampling_period)

    camera.start()
    #control.start()

    control.generate_transform()
    control.target((0,0))
    time.sleep(1)

    #t = threading.Thread(target=read_input)
    #t.start()

    #obj = Identification()

    try:
        while True:
            #x = float(input("x: "))
            #y = float(input("y: "))
            #obj.position = (x,y)
            #control.update_positions(obj, camera.laser)

            control.target(camera.object.position)
            time.sleep(sampling_period)
    except(KeyboardInterrupt):
        pass
    finally:
        run = False
        control.stop()
        camera.stop()

        #control.join()
        #camera.join()

        pi.stop()

def read_input():
    global x, y, run
    while run:
        p = input()
        xx, yy = p.split(' ')
        x, y = float(xx), float(yy)

if __name__ == "__main__":
    main()