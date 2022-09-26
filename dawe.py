from websocket import WebSocket
def connect_room(socket: WebSocket, room_id: str):
    message = '{"type":"joinroom","roomId":"'+ room_id +'"}'
    socket.send(message)