from fastapi import FastAPI, Form, Request, HTTPException
import uvicorn
import requests
import redis
import os

if 'SERVER_NUMBER' in os.environ:
    server_number = os.environ['SERVER_NUMBER']
else:
    server_number = '1'

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
    server_number = 1

    def __init__(self, redis_host, redis_port, server_number):
        self.redis_port = 6379
        self.redis_host = redis_host
        self.server_number = server_number
        self.instance = redis.Redis(host = redis_host, port = redis_port, db = 0)
        self.instance.rpush('log', server_number + " default")

    def reconnect(self):
        self.instance = redis.Redis(host = self.redis_host, port = self.redis_port, db = 0)

    def get_instance(self):
        if self.instance == None:
            self.reconnect()
        return self.instance
    
    def update_log(self, log_str:str):
        self.reconnect()
        self.instance.rpush('log', server_number + " " + log_str)
    
    def get_log(self):
        self.reconnect()
        return self.instance.lrange('log', 0, -1)
    def clear(self):
        self.reconnect()
        while(self.instance.llen('log')!=0):
            self.instance.lpop('log')



app = FastAPI()
db = Database(redis_host=redis_host, redis_port=redis_port,server_number=server_number)

@app.get("/")
def get_logs():
    server_log = db.get_log()
    if server_log != None:
        str_all = ""
        for s in server_log:
            str_all += s.decode('utf-8') + '\n'
        return {"log" : str_all}
    raise HTTPException(status_code = 404, detail="error getting logs from server")


@app.post("/")
def update_logs(s:str):

    if s == "clear":
        try:
            db.clear()
        except:
            raise HTTPException(status_code = 404, detail="error clearing logs from server")
        return
    try:
        db.update_log(log_str=s)
        return {"message" : "update ok"}
    except:
        raise HTTPException(status_code = 404, detail="error updating logs from server")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=1323, log_level="info")
