import RPi.GPIO as GPIO

# Handles controlling the DC motor connected to Pi.
class Driver:
    def __init__(self, PWM_PIN):
        GPIO.setwarnings(False)

        self.IN_1_PIN = 24
        self.IN_2_PIN = 25

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PWM_PIN, GPIO.OUT)
        GPIO.setup(self.IN_1_PIN, GPIO.OUT)
        GPIO.setup(self.IN_2_PIN, GPIO.OUT)

        # We want the disc to spin at the correct speed clockwise. If voltage is positive, we're adding clockwise
        # torque, else we're adding anticlockwise torque.
        self.set_clockwise()

        self.pwm = GPIO.PWM(PWM_PIN, 4000)
        self.pwm.start(0)

        self.max_voltage = 10 # The maximum voltage we can supply to our motor.

        return

    def set_clockwise(self):
        GPIO.output(self.IN_1_PIN, GPIO.HIGH)
        GPIO.output(self.IN_2_PIN, GPIO.LOW)
        return

    def set_anti_clockwise(self):
        GPIO.output(self.IN_1_PIN, GPIO.LOW)
        GPIO.output(self.IN_2_PIN, GPIO.HIGH)
        return

    def set_voltage(self, voltage):
        # Firstly, clamp this voltage to between -10V and 10V.
        voltage = max(min(self.max_voltage, voltage), -10)

        # If the voltage is negative, we need to invert the direction.
        if voltage < 0:
            self.set_anti_clockwise()
            voltage = voltage * -1
        else:
            self.set_clockwise()

        print('Setting voltage to: ' + str(voltage))

        # Calculate this voltage as a percentage duty cycle:
        duty_cycle = (voltage / self.max_voltage) * 100

        print('Setting duty cycle to: ' + str(duty_cycle))

        self.pwm.ChangeDutyCycle(duty_cycle)
        return duty_cycle

    def stop(self):
        self.pwm.stop()
        GPIO.cleanup()
        return
