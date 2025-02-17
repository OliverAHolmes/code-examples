from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import jwt
from pathlib import Path


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
public_key = (Path(__file__).parent / "../backend/app/public_key.pem").read_text()
ALGORITHM = "RS256"
http_bearer = HTTPBearer()

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
    print(token)
    try:
        print(public_key)
        payload = jwt.decode(token, public_key, algorithms=[ALGORITHM])
        print('my test')

        print(payload)
        return payload
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid token")

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