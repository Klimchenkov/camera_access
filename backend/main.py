import os 
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError,ConnectionClosedOK
from camera import Camera


app = FastAPI()
camera = Camera(os.environ.get("CAMERA_URL", 0))
connections = {}


@app.websocket("/ws")
async def broadcast(websocket: WebSocket):
    await websocket.accept()
    connections[websocket['client']] = 1
    if not camera.is_running:
        camera.start()
    try:
        while True:
            frame = camera.current_frame
            if frame is not None:
                await websocket.send_bytes(frame.tobytes()) 
    except (WebSocketDisconnect, ConnectionClosedError, ConnectionClosedOK):
        print(f"Client {websocket['client']} disconnected")   
        del connections[websocket['client']]
        if not connections:
            camera.stop()


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)