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

@sio.on('*')
async def catch_all(event, sid, data):
    await sio.emit(event, data, skip_sid=sid)
    pass

if __name__ == '__main__':
    web.run_app(app)
