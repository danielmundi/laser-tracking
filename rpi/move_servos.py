import pigpio
import time

def main():
    pi = pigpio.pi()
    pi.set_mode(12, pigpio.OUTPUT)

    n = 0
    #time.sleep(2)
    try:
        while n >= 0:
            n = float(raw_input("DC: "))
            #pi.hardware_PWM(12, 33, n*10000)
            pi.hardware_PWM(12, 33, angle2duty(n)*10000)
            #print(str((n)))
            print(str(angle2duty(n)))
    except (KeyboardInterrupt):
        pass
    finally:
        pi.hardware_PWM(12, 0, 0)
        pi.stop()

def angle2duty(angle):
    duty = angle*(7.3-2)/(180) + 2
    return duty #int(duty*10)/10.0

if __name__ == "__main__":
    main()
