import RPi.GPIO as GPIO
import time
from ControlComponents.Controller import Controller
from ControlComponents.Driver import Driver
from ControlComponents.WebsocketServer import WebsocketServer

INTERRUPT_PIN = 23
PWM_PIN = 12

# Set up the interrupt and PWM pins:
GPIO.setmode(GPIO.BCM)
GPIO.setup(INTERRUPT_PIN, GPIO.IN)

controller = Controller() # The PID controller for this.
driver = Driver(PWM_PIN) # Handles controlling the motor attached to the Pi.
server = WebsocketServer(controller) # The websocket server.

# Each time we measure a rotation, we know the updated speed of the disc and can adjust the error accordingly:
# Note - we need to time this operation to ensure that it can be executed before the next interrupt occurs:
def rotation_completed(channel):
    # Update the current speed in the motor
    controller.update_current_speed()

    # This converts the error to a voltage input to the moto.
    voltage_output = controller.get_voltage_output()

    print(voltage_output)

    # Clamp the voltage to between 0V and 10V and convert it to a duty cycle.
    duty_cycle = driver.set_voltage(voltage_output)

    print(duty_cycle)

    # Emit this event to our connected clients:
    server.emit_measured_speed()
    return True

# Add an interrupt to calculate the speed on each rotation.
GPIO.add_event_detect(INTERRUPT_PIN, GPIO.RISING, callback=rotation_completed, bouncetime=100)

# Keep the program running, as we are only relying on interrupts.
try:
    while True:
        None
except KeyboardInterrupt:
    pass

driver.stop()
server.close()