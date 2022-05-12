import math
import time
import os

class Controller:
    def __init__(self):
        self.DISC_DIAMETER = 0.395
        self.DISC_CIRCUMFERENCE = math.pi * self.DISC_DIAMETER
        self.NO_OF_REFERENCES = 2

        self.current_speed = 0 # The speed the disc is currently going.
        self.last_recorded_time = self.get_current_time() # The time the last click was recorded at.

        self.TARGET = 10 # The km/h speed that we want the disc to spin at.

        self.time_elapsed = 0 # Equivalent to the sampling time (how long it was between the last two errors).

        # Record the last 3 errors and inputs:
        self.e0 = 0 # Current error
        self.e1 = 0 # e^-1
        self.e2 = 0 # e^-2
        self.u0 = 0
        self.u1 = 0
        self.u2 = 0

        # The tuned values for this PID controller:
        #self.Kp = 0.422615
        self.Kp = 5.922615
        self.Ki = 0.019689
        #self.Ki = 0.00002
        self.Kd = 0.161528
        self.N = 7.709

    # Gets the current time in milliseconds.
    def get_current_time(self):
        return round(time.time() * 1000)

    # Update the current_speed variable on each new tick:
    def update_current_speed(self):
        current_time = self.get_current_time()
        self.time_elapsed = (current_time - self.last_recorded_time) / 1000

        multiplier = 1 / self.time_elapsed  # Convert milliseconds to seconds.
        self.current_speed = ((self.DISC_CIRCUMFERENCE / self.NO_OF_REFERENCES) * multiplier) * 3.6  # * 3.6 converts m/s to km/h.

        # Save the last_recorded time as the most recently used time:
        self.last_recorded_time = current_time

        os.system('cls' if os.name == 'nt' else 'clear')
        print('Current speed: ' + str(self.current_speed))

        return self.current_speed

    def get_error(self):
        return self.TARGET - self.current_speed

    # Returns the voltage output as calculated by the PID controller:
    def get_voltage_output(self):
        self.e0 = self.get_error()
        print('Error:')
        print(self.e0)

        # Shorten these here to clean up the eqns.
        N = self.N
        Ki = self.Ki
        Kp = self.Kp
        Kd = self.Kd
        Ts = self.time_elapsed # Get the sampling time.

        # Get the constants for the equation:
        a0 = (1 + N * Ts)
        a1 = -(2 + (N * Ts))
        a2 = 1

        b0 = Kp * (1 + N * Ts) + (Ki * Ts) * (1 + N * Ts) + (Kd * N)
        b1 = -(Kp * (2 + N * Ts) + Ki * Ts + 2 * Kd * N)
        b2 = Kp + Kd * N


        ku1 = a1 / a0
        ku2 = a2 / a0
        ke0 = b0 / a0
        ke1 = b1 / a0
        ke2 = b2 / a0

        self.e2 = self.e1
        self.e1 = self.e0
        self.u2 = self.u1
        self.u1 = self.u0

        self.u0 = -ku1 * self.u1 - ku2 * self.u2 + ke0 * self.e0 + ke1 * self.e1 + ke2 * self.e2
        print(self.u0)
        return self.u0

    def set_target(self, target):
        self.TARGET = target
        return

    def set_gain_values(self, data):
        self.Kp = float(data['proportional'])
        self.Ki = float(data['integral'])
        self.Kd = float(data['derivative'])
        return True