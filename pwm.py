import RPi.GPIO as GPIO
import time


PWM_PIN = 12
IN_1_PIN = 24
IN_2_PIN = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)
GPIO.setup(IN_1_PIN, GPIO.OUT)
GPIO.setup(IN_2_PIN, GPIO.OUT)
p = GPIO.PWM(PWM_PIN, 1000)

GPIO.output(IN_1_PIN,GPIO.HIGH)
GPIO.output(IN_2_PIN,GPIO.LOW)

p.start(50)

try:
        while True:
                time.sleep(0.02)
                for i in range(100):
                        #p.ChangeDutyCycle(i)
                        time.sleep(0.02)
                for i in range(100):
                        #p.ChangeDutyCycle(100-i)
                        time.sleep(0.02)
except KeyboardInterrupt:
        pass

p.stop()

GPIO.cleanup()