import pigpio
import time

def main():
    laser_pin = 16
    motorx_pin = 12
    motory_pin = 13
    pi = pigpio.pi()
    pi.set_mode(motorx_pin, pigpio.OUTPUT)  # motor x
    pi.set_mode(motory_pin, pigpio.OUTPUT)  # motor x
    pi.set_mode(laser_pin, pigpio.OUTPUT)  # laser

    pi.set_pull_up_down(laser_pin, pigpio.PUD_DOWN)
    pi.write(laser_pin, 1)

    n = 0
    #time.sleep(2)
    try:
        while n >= 0:
            s = input("DC: ")
            n = float(s)
            #i, n = s.split(' ')
            #i, n = int(i), float(n)
            i = 1
            if i == 1:
                pi.hardware_PWM(motorx_pin, 50, int(angle2duty(n)*10000))
                #pi.hardware_PWM(motorx_pin, 50, int(n*10000))
            else:
                pi.hardware_PWM(motory_pin, 50, int(angle2duty(n)*10000))
                #pi.hardware_PWM(motory_pin, 50, int(n*10000))
            #print(str((n)))
            print(str(angle2duty(n)))
    except (KeyboardInterrupt):
        pass
    finally:
        pi.hardware_PWM(motorx_pin, 0, 0)
        pi.hardware_PWM(motory_pin, 0, 0)
        pi.write(laser_pin, 0)
        pi.stop()

def angle2duty(angle):
    duty = angle*(11.1-3)/(180) + 3
    return duty #int(duty*10)/10.0

if __name__ == "__main__":
    main()
