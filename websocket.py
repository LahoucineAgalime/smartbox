from types import CellType
from redis import DataError
from sanic import Sanic
import enum
from sanic.response import json
import json as JSON


from datetime import datetime
app = Sanic("websocket")

clients = []


class State(enum.IntEnum):
    CONNECTING, OPEN, CLOSING, CLOSED = range(4)


CONNECTING = State.CONNECTING
OPEN = State.OPEN
CLOSING = State.CLOSING
CLOSED = State.CLOSED


@app.websocket('/ws/notice')
async def notice(request, ws):
    clients.append(ws)
    while True:
        data = await ws.recv()
        await ws.send(f'receive data:{data} server response:ok')


@app.route('alert', methods=["POST", ])
async def alert(request):
    msg = request.form.get('msg')
    t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for client in clients:
        if client.connection.state in (CLOSED, CLOSING):
            clients.remove(client)
        data = {
            'message': msg,
            'time': t,
            'online': len(clients)
        }
        await client.send(JSON.dumps(data, ensure_ascii=False))
    return json({'msg': 'ok'})

app.config.WEBSOCKET_MAX_SIZE = 2 ** 20
app.config.WEBSOCKET_MAX_QUEUE = 32
app.config.WEBSOCKET_READ_LIMIT = 2 ** 16
app.config.WEBSOCKET_WRITE_LIMIT = 2 ** 16
app.config.WEBSOCKET_PING_INTERVAL = 20
app.config.WEBSOCKET_PING_TIMEOUT = 20
app.run(port=8001)
