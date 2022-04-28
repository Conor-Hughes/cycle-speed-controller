import RPi.GPIO as GPIO
import time
import math
from ControlComponents.Controller import Controller
from ControlComponents.Driver import Driver
from ControlComponents.WebsocketClient import WebsocketClient
from ControlComponents.Tuner import Tuner
from pprint import pprint

INTERRUPT_PIN = 23
PWM_PIN = 12

# Set up the interrupt and PWM pins:
GPIO.setmode(GPIO.BCM)
GPIO.setup(INTERRUPT_PIN, GPIO.IN)

controller = Controller() # The PID controller for this.
driver = Driver(PWM_PIN) # Handles controlling the motor attached to the Pi.
tuner = Tuner(driver)
ws_client = WebsocketClient(controller, tuner=tuner) # The websocket client to communicate with the WSS.

global bounce
bouncetime = 60

def run_interrupt(channel):
    # Check that the previous bouncetime has expired:
    let

# Each time we measure a rotation, we know the updated speed of the disc and can adjust the error accordingly:
# Note - we need to time this operation to ensure that it can be executed before the next interrupt occurs:
def rotation_completed(channel):
    # We only want to run this when the tuner is currently enabled (e.g. it's running a sim.)
    if tuner.enabled:
        # Update the current speed in the motor
        controller.update_current_speed()

        # This converts the error to a voltage input to the moto.
        voltage_output = controller.get_voltage_output()

        # Clamp the voltage to between 0V and 10V and convert it to a duty cycle.
        duty_cycle = driver.set_voltage(voltage_output)

        # Add this current speed along with the timestamp to the tuner results:
        tuner.add_result(controller.current_speed, controller.last_recorded_time / 1000)

    return True

# Add an interrupt to calculate the speed on each rotation.
e = GPIO.add_event_detect(INTERRUPT_PIN, GPIO.RISING, callback=rotation_completed, bouncetime=0)

pprint(vars(GPIO))

# Keep the program running, as we are only relying on interrupts.
try:
    while True:
        None
except KeyboardInterrupt:
    pass

driver.stop()
ws_client.close()