import pigpio

def main():
    pi = pigpio.pi()
    pi.set_mode(12, pigpio.OUTPUT)

    n = 0
    try:
        while n >= 0:
            n = float(raw_input("Angle: "))
            pi.hardware_PWM(12, 40, angle2duty(n)*10000)
            print(str(angle2duty(n)))
    except (KeyboardInterrupt):
        pass
    finally:
        pi.hardware_PWM(12, 0, 0)
        pi.stop()

def angle2duty(angle):
    duty = angle*(15.1-0.1)/(120) + 0.1
    return int(duty*10)/10.0

if __name__ == "__main__":
    main()
