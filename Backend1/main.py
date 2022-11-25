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
    redis_port = 6379


class Database:
    instance = None
    redis_host = 'localhost'
    redis_port = 6379

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

    def clear(self):
        self.instance.set('sum', None)
        self.instance.set('cnt', None)
        self.instance.set('max_value', None) 
    
    def update(self, x:int):
        self.reconnect()
        
        sum = self.instance.get('sum')
        cnt = self.instance.get('cnt')
        mx = self.instance.get('max_value')
        if sum == None or cnt == None:
            sum, cnt = 0, 0
        
        if cnt == 0:
            mx = x
        else: 
            sum = int(sum)
            cnt = int(cnt)
            mx = int(mx)
            mx = max(mx, x)
        sum += x
        cnt += 1
        self.instance.set('cnt', cnt)
        self.instance.set('sum', sum)
        self.instance.set('max_value', mx)
        self.instance.rpush('value_list', x)



app = FastAPI()
db = None
try :
    db = Database(redis_host=redis_host, redis_port=redis_port)
except:
    db = None

@app.post("/")
def insert_value(x:str):
    global db
    if db == None:
        try:
            db = Database(redis_host=redis_host, redis_port=redis_port)
        except:
            raise HTTPException(status_code = 500, detail="error connecting to db")
    try:
        if x == 'clear':
            db.clean(x)
        else:     
            db.update(int(x))
        return {"message" : "ok"}
    except:
        raise HTTPException(status_code = 500, detail="error inserting value to db")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1323, log_level="info")
