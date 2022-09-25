import asyncio
import websockets
import json
import numpy as np
from win32helper import setColorizationColor

SOCKET_ADDR = 'localhost'
SOCKET_PORT = 55001
DATA_PATH = 'wpe.json'
data = None

def calcImage(path):
    import cv2
    # workaround for non-ascii path
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    m = cv2.mean(img)
    return round(m[0]), round(m[1]), round(m[2])

async def handler(websocket, uri):
    async for message in websocket:
        # recieve image path
        path = message  # type: str
        path = path.replace('%3A', ':')
        if path not in data:
            color = calcImage(path)
            # save color
            data[path] = color
            file = open(DATA_PATH, 'w')
            file.write(json.dumps(data, indent=1))
            file.close()
        r, g, b = data[path]
        ok = setColorizationColor(r, g, b)
        # print("{}: {},{},{} {}".format(path, r, g, b, ok))

async def main():
    async with websockets.serve(handler, SOCKET_ADDR, SOCKET_PORT):
        # run forever
        await asyncio.Future()

if __name__ == '__main__':
    file = open(DATA_PATH, 'r')
    data = json.loads(file.read())
    file.close()
    asyncio.run(main())
