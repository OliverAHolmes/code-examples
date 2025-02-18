from robyn import Robyn

app = Robyn(__file__)

@app.get("/robyn")
async def hello():
    return {"message": "Hello, world!"}

app.start(port=8000, host="0.0.0.0")