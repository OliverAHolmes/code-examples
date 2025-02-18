# main.py (FastAPI)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import requests
import time

from jose import jwt, jwk
from jose.utils import base64url_decode

JWKS_URL = "http://127.0.0.1:8000/.well-known/jwks.json"
ALGORITHM = "RS256"

app = FastAPI()
http_bearer = HTTPBearer()

# Add CORS middleware if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

def get_jwks():
    """
    Simple fetch of JWKS from Django.
    In production, you might want to cache or periodically refresh
    to avoid fetching on every request.
    """
    resp = requests.get(JWKS_URL)
    resp.raise_for_status()  # If the URL fails, raise an error
    return resp.json()

def get_signing_key(token: str, jwks: dict):
    """
    If you have multiple keys in the JWKS, you typically match the 'kid'
    in the JWT header to the correct JWK in the list.
    This example uses a single key (no kid).
    """
    # Extract unverified header first
    unverified_header = jwt.get_unverified_header(token)
    token_kid = unverified_header.get('kid')

    # If your JWKS only has one key, we can assume that's the key.
    # If you do have multiple keys, you'd do:
    # matching_keys = [k for k in jwks['keys'] if k.get('kid') == token_kid]
    # if not matching_keys: raise ...
    # key_dict = matching_keys[0]
    key_dict = jwks["keys"][0]  # Single JWK scenario

    return key_dict

async def verify_token(token: str):
    """
    1. Fetch JWK from Django
    2. Validate signature
    3. (Optionally) validate standard claims like 'exp', 'iat', 'aud', etc.
    """
    jwks = get_jwks()
    key_dict = get_signing_key(token, jwks)

    # python-jose: verify the signature ourselves:
    public_rsa_key = jwk.construct(key_dict)

    # The token has the structure header.payload.signature
    message, signature = token.rsplit('.', 1)
    decoded_signature = base64url_decode(signature.encode())

    if not public_rsa_key.verify(message.encode(), decoded_signature):
        raise HTTPException(status_code=401, detail="Invalid token signature")

    # If signature is valid, let's decode payload without verifying again
    # (but let's at least check exp manually for safety)
    unverified_claims = jwt.get_unverified_claims(token)
    if "exp" in unverified_claims and unverified_claims["exp"] < time.time():
        raise HTTPException(status_code=401, detail="Token expired")

    return unverified_claims

@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    """
    WebSocket endpoint that requires a valid JWT token (RS256).
    The token is included in the path here for simplicity
    (or you could use a query parameter, subprotocol, etc.).
    """
    try:
        payload = await verify_token(token)
        user_id = payload.get("user_id", "unknown")

        await manager.connect(websocket)
        await manager.broadcast(f"User {user_id} joined")
        try:
            while True:
                data = await websocket.receive_text()
                await manager.send_personal_message(f"Echo: {data}", websocket)
        except WebSocketDisconnect:
            manager.disconnect(websocket)
            await manager.broadcast(f"User {user_id} left the chat")
    except HTTPException:
        await websocket.close(code=1008)  # Policy Violation / invalid token
