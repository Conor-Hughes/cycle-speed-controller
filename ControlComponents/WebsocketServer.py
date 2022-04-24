from aiohttp import web, WSCloseCode
import socketio

class WebsocketServer:
    def __init__(self, controller):

        # These are configured later on.
        self.sio = None
        self.app = None
        self.site = None

        # Configures an async aiohttp server with attached socket.io.
        self.configure_server()

        self.controller = controller # The PID controller.

    async def configure_server(self):
        # Create a new async Socket.io Server:
        self.sio = await socketio.AsyncServer(cors_allowed_origins="*")

        # Create a new aiohttp web app:
        self.app = web.AppRunner()
        await app.setup()

        # Bind the socket.io instance to the web app instance:
        await self.sio.attach(self.app)
        self.site = web.TCPSite(self.app, 'localhost', 8080)
        await self.site.start()

        @self.sio.event
        def connect(sid, environ, auth):
            print('Connected: ', sid)

        @self.sio.event
        def disconnect(sid):
            print('Disconnected: ', sid)

        @self.sio.on('update_target')
        async def update_target_speed(sid, message):
            self.controller.set_target(message) # In reality, this would be validated.

        while True:
            await asyncio.sleep(3600)  # sleep forever

    # Emits the measured speed to connected clients.
    def emit_measured_speed(self):
        print('Emitting speed! ' + str(self.controller.current_speed))
        return self.sio.emit('measured_speed', {'speed': self.controller.current_speed})

    async def close(self):
        await self.app.cleanup()