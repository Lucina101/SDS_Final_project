from fastapi import FastAPI, Form, Request, HTTPException
import uvicorn
import requests
import redis
import os

if 'REDIS_HOST' in os.environ:
    redis_host = os.environ['REDIS_HOST']
else:
    redis_host = "localhost"

if 'REDIS_PORT' in os.environ:
    redis_port = os.environ['REDIS_PORT']
else:
    redis_port = 6397


class Database:
    instance = None
    redis_host = 'localhost'
    redis_port = 6397

    def __init__(self, redis_host, redis_port):
        self.redis_port = 6379
        self.redis_host = redis_host
        self.instance = redis.Redis(host = redis_host, port = redis_port, db = 0)

    def reconnect(self):
        self.instance = redis.Redis(host = self.redis_host, port = self.redis_port, db = 0)

    def get_instance(self):
        if self.instance == None:
            self.reconnect()
        return self.instance
    
    def get_maximum(self):
        self.reconnect()
        mx = self.instance.get('max_value')        
        return mx


app = FastAPI()
db = None
try :
    db = Database(redis_host=redis_host, redis_port=redis_port,server_number=server_number)
except:
    db = None

@app.get("/")
def get_maximum():
    global db
    if db == None:
        try:
            db = Database(redis_host=redis_host, redis_port=redis_port)
        except:
            raise HTTPException(status_code = 500, detail="error connecting to db")
    
    mx = db.get_maximum()
    if mx != None:
        return {"maximum" : int(mx)}
    raise HTTPException(status_code = 400, detail="error getting maximum from db")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1325, log_level="info")
