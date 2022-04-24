import RPi.GPIO as GPIO

# Handles controlling the DC motor connected to Pi.
class Driver:
    def __init__(self, PWM_PIN):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PWM_PIN, GPIO.OUT)
        self.pwm = GPIO.PWM(PWM_PIN, 8000)
        self.pwm.start(0)

        self.max_voltage = 10 # The maximum voltage we can supply to our motor.

        return

    def set_voltage(self, voltage):
        # Firstly, clamp this voltage to between 0 and 10V.
        voltage = max(min(self.max_voltage, voltage), 0)

        # Calculate this voltage as a percentage duty cycle:
        duty_cycle = (voltage / self.max_voltage) * 100

        self.pwm.ChangeDutyCycle(duty_cycle)
        return duty_cycle

    def stop(self):
        self.pwm.stop()
        GPIO.cleanup()
        return
