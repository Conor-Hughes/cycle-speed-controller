import math
import time
import os

class Controller:
    def __init__(self):
        self.DISC_DIAMETER = 0.395
        self.DISC_CIRCUMFERENCE = math.pi * self.DISC_DIAMETER

        self.current_speed = 0 # The speed the disc is currently going.
        self.last_recorded_time = self.get_current_time() # The time the last click was recorded at.

        self.TARGET = 15 # The km/h speed that we want the disc to spin at.
        self.previous_error = 0; # Save the last logged error value so we can use derivative control.
        self.sum_of_errors = 0; # Save the total value of errors to be used for integral control.

        # The tuned values for this PID controller:
        self.Kp = 0.422615
        self.Ki = 0.029689
        self.Kd = 0.091528

    # Gets the current time in milliseconds.
    def get_current_time(self):
        return round(time.time() * 1000)

    # Update the current_speed variable on each new tick:
    def update_current_speed(self):
        current_time = self.get_current_time()
        time_elapsed = current_time - self.last_recorded_time

        multiplier = 1 / (time_elapsed / 1000)  # Convert milliseconds to seconds.
        self.current_speed = (self.DISC_CIRCUMFERENCE * multiplier) * 3.6  # * 3.6 converts m/s to km/h.

        # Save the last_recorded time as the most recently used time:
        self.last_recorded_time = current_time

        os.system('cls' if os.name == 'nt' else 'clear')
        print('Current speed: ' + str(self.current_speed))

        return self.current_speed

    def get_error(self):
        return self.TARGET - self.current_speed

    # Returns the voltage output as calculated by the PID controller:
    def get_voltage_output(self):
        error = self.get_error()
        voltage = (error * self.Kp) + (self.previous_error * self.Kd) + (self.sum_of_errors * self.Ki)
        self.previous_error = error
        self.sum_of_errors += error
        return voltage