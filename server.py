
import websockets
import os 
from http import HTTPStatus
import datetime
import asyncio
import random 
import functools

clients = set()

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

    # Derive full system path
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
    clients.add(websocket)
    while websocket.open:
        # now = datetime.datetime.utcnow().isoformat() + 'Z'
        message = await websocket.recv()
        for ws in clients:
            await ws.send(message)
    # This print will not run when abrnomal websocket close happens
    # for example when tcp connection dies and no websocket close frame is sent
    print("WebSocket connection closed for", websocket.remote_address)


def run_server(port: int):
    handler = functools.partial(process_request, os.getcwd())

    start_server = websockets.serve(time, '127.0.0.1', port,
                                    process_request=handler)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

# import asyncio
# from websockets import serve

# connected = set()

# async def handler(websocket, path):
#     data = await websocket.recv()
#     connected.add(websocket)
#     print(len(connected))
#     for socket in connected:
#         print("sending data: " + data)
#         await socket.send(data)


# async def run(port: int):
#     async with serve(handler, "localhost", port):
#         await asyncio.Future()  # run forever
# def run_server(port: int):
#     asyncio.run(run(port))

# from simple_websocket_server import WebSocketServer
# from simple_websocket_server import WebSocket as WebSocketS
# class WebServer(WebSocketS):
#     def handle(self):
#         # echo message back to client
#         for client in clients:
#             if client != self:
#                 client.send_message(self.data)

#     def connected(self):
#         print(self.address, 'connected')
#         clients.append(self)

#     def handle_close(self):
#         clients.remove(self)
# clients = []

# def run_server(port: int):
#     server = WebSocketServer('', port, WebServer)
#     server.serve_forever()