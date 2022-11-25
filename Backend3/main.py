from fastapi import FastAPI, Form, Request, HTTPException
import uvicorn
import requests
import redis
import os

if "REDIS_HOST" in os.environ:
    redis_host = os.environ['REDIS_HOST']
else:
    redis_host = 'localhost'

if "REDIS_PORT" in os.environ:
    redis_port = os.environ['REDIS_PORT']
else:
    redis_port = "6379"

app = FastAPI()

@app.get("/")
def insert(x:int):
    return


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1323, log_level="info")
