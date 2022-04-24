from aiohttp import web
import socketio

sio = socketio.AsyncServer(cors_allowed_origins="*")
app = web.Application()
sio.attach(app)

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('target_speed')
async def set_target_speed(sid, message):
    print(message)

    # Send this target speed to the driver.
    sio.emit('target_speed', message, skip_sid=sid)
    pass

@sio.on('measured_speed')
async def send_measured_speed(sid, message):
    print(message)

    # Send this measured speed to the client.
    sio.emit('measured_speed', message, skip_sid=sid)
    pass

if __name__ == '__main__':
    web.run_app(app)
