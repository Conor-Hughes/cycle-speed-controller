import socketio

class WebsocketClient:
    def __init__(self, controller, tuner=None):

        self.controller = controller

        # Connect to the WSS:
        self.sio = socketio.Client()

        @self.sio.event
        def connect():
            print('Connected to WSS.')

        # If this WSClient is being used for tuner.py:
        if tuner is not None:

            self.tuner = tuner

            @self.sio.event
            def start(data):
                print('Receiving start event...')

                # Set the gain values inside the controller:
                print(type(data))
                self.controller.set_gain_values(data)
                self.controller.set_target(int(data['stepInput']))

                # Set the start time of the tuner & set it to enabled to begin the sim.
                self.tuner.handle_start_event()

            @self.sio.event
            def stop_sim(data):
                print('Receiving stop event...')

                self.sio.emit('results', {
                    "started_at": self.tuner.sim_started_at,
                    "results": self.tuner.results
                })

                self.tuner.handle_stop_event()

        # If it's being used for main.py:
        else:
            @self.sio.event
            def target_speed(data):
                print('Setting target speed...')
                controller.set_target(data)

        # Connects to server and sets up listener for changes in target speed.
        self.connect_to_wss()

        pass

    def get_sio(self):
        return self.sio

    def connect_to_wss(self):
        return self.sio.connect('http://0.0.0.0:8080')

    def send_measured_speed(self):
        return self.sio.emit('measured_speed', {'measured_speed': self.controller.current_speed})

    def close(self):
        self.sio.disconnect()
        return
