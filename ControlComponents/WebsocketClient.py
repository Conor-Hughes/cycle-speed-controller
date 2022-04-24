import socketio

class WebsocketClient:
    def __init__(self, controller):

        self.controller = controller

        # Connect to the WSS:
        self.sio = socketio.Client()

        # Connects to server and sets up listener for changes in target speed.
        self.connect_to_wss()

        pass

    def connect_to_wss(self):
        self.sio.connect('http://0.0.0.0:8080')

        @self.sio.event
        def connect():
            print("Connected to the WSS.")

        @self.sio.event
        def target_speed(data):
            self.controller.set_target(data.target)

        return

    def send_measured_speed(self):
        return self.sio.emit('measured_speed', {'measured_speed': self.controller.current_speed})

    def close(self):
        self.sio.disconnect()
        return
