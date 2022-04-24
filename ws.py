from aiohttp import web
import socketio
import RPi.GPIO as io
import random
import asyncio
import time

# Configure the LED inputs and outputs:
io.setmode(io.BCM)
yellow = 27
blue = 22
io.setup(yellow, io.OUT)
io.setup(blue, io.OUT)
io.output(yellow, False)
io.output(blue, False)

# creates a new Async Socket IO Server
sio = socketio.AsyncServer(cors_allowed_origins="*")
# Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App instance
sio.attach(app)

desired_speed = 0

@sio.event
def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.on('desired_speed')
async def set_desired_speed(sid, message):
    print(type(message))
    desired_speed = message
    await sio.emit('measured_speed', random.randrange(int(desired_speed) - 5, int(desired_speed) + 5))
    print('Desired speed updated to: ' + str(desired_speed))

# Define a coroutine to send the measured speed to the browser every 0.25s:
# def periodic(period):
#     def scheduler(fcn):
#
#         async def wrapper(*args, **kwargs):
#
#             while True:
#                 asyncio.create_task(fcn(*args, **kwargs))
#                 await asyncio.sleep(period)
#
#         return wrapper
#
#     return scheduler


# @periodic(2)
# async def do_something(*args, **kwargs):
#     print('Emitting measured_speed')
#     sio.emit('measured_speed', random.randrange(desired_speed - 5, desired_speed + 5))

if __name__ == '__main__':
    # asyncio.run(do_something('Maluzinha do papai!', secret=42))
    web.run_app(app)