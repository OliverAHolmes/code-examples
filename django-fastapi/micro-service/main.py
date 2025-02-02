from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import jwt

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT settings (must match Django's settings)
JWT_SECRET = "your-secret-key"  # Use the same secret key as in Django
ALGORITHM = "HS256"

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

async def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# @app.websocket("/ws-echo")
# async def echo_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     print("connection open")
#     try:
#         while True:
#             data = await websocket.receive_text()
#             print("received:", data)
#             await websocket.send_text(f"Echo: {data}")
#     except WebSocketDisconnect:
#         print("connection closed")

@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    try:
        # Verify token first
        payload = await verify_token(token)
        
        # Define user_id once, so it's in scope for the entire function
        user_id = payload.get("user_id")

        # Accept and connect
        await manager.connect(websocket)
        
        try:
            while True:
                data = await websocket.receive_text()
                await manager.send_personal_message(f"Echo: {data}", websocket)
        except WebSocketDisconnect:
            # This block will run when the user disconnects
            manager.disconnect(websocket)
            await manager.broadcast(f"User {user_id} left the chat")

    except HTTPException:
        # Close with a Policy Violation code if token invalid/expired
        await websocket.close(code=1008)