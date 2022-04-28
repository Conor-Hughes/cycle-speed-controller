import time

class Tuner:
    def __init__(self, driver):
        self.enabled = False
        self.sim_started_at = None
        self.results = {}

        self.driver = driver

    def add_result(self, result, time):
        self.results[time] = result

    # This is called when the websocket triggers a start event. We want to set the property to enabled so that interrupts
    # will now take over and handle getting it to the right speed, and set an internal property to let us know what time this
    # simulation started. We also want to set the driver to put the motor running at full speed to start it off.
    def handle_start_event(self):
        self.enabled = True
        self.sim_started_at = time.time()
        self.driver.set_voltage(10)

    # This handles removing the enabled flag so that interrupts are stopped from calling.
    # The websocket has already handled sending the sim start time + the results to the browser, so we can reset them
    # here.
    def handle_stop_event(self):
        self.driver.set_voltage(0)
        self.enabled = False
        self.sim_started_at = None
        self.results = {}