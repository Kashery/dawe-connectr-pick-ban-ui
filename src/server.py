
import websockets
import os 
from http import HTTPStatus
import datetime
import asyncio
import random 
import functools

clients = {}

MIME_TYPES = {
    "html": "text/html",
    "js": "text/javascript",
    "css": "text/css",
    "jpg":"image/jpeg"
}

async def process_request(sever_root, path, request_headers):
    """Serves a file when doing a GET request with a valid path."""

    if "Upgrade" in request_headers:
        return  # Probably a WebSocket connection

    if path == '/':
        path = '/index.html'

    response_headers = [
        ('Server', 'asyncio websocket server'),
        ('Connection', 'close'),
    ]

    full_path = os.path.realpath(os.path.join(sever_root, path[1:]))

    # Validate the path
    if os.path.commonpath((sever_root, full_path)) != sever_root or \
            not os.path.exists(full_path) or not os.path.isfile(full_path):
        # print("HTTP GET {} 404 NOT FOUND".format(path))
        return HTTPStatus.NOT_FOUND, [], b'404 NOT FOUND'

    # Guess file content type
    extension = full_path.split(".")[-1]
    mime_type = MIME_TYPES.get(extension, "application/octet-stream")
    response_headers.append(('Content-Type', mime_type))

    # Read the whole file into memory and send it out
    body = open(full_path, 'rb').read()
    response_headers.append(('Content-Length', str(len(body))))
    # print("HTTP GET {} 200 OK".format(path))
    return HTTPStatus.OK, response_headers, body



async def time(websocket, path):
    if path not in clients:
        clients[path] = set()
    clients[path].add(websocket)
    while websocket.open:
        try:
            message = await websocket.recv()
            for ws in clients[path]:
                await ws.send(message)
        except:
            clients[path].remove(websocket)
            

def run_server(port: int):
    handler = functools.partial(process_request, os.getcwd())

    start_server = websockets.serve(time, '127.0.0.1', port,
                                    process_request=handler)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()