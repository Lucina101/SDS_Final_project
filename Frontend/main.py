import pathlib

from fastapi import FastAPI, Form, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

import uvicorn
import requests
import os

if 'SERVER_HOST' in os.environ:
    server_host = os.environ['SERVER_HOST']
else :
    server_host = 'localhost'

if 'SERVER_PORT' in os.environ:
    server_port = os.environ['SERVER_PORT']
else:
    server_port = 1323
app = FastAPI()

BASE_DIR = pathlib.Path(__file__).parent # src
templates = Jinja2Templates(directory = BASE_DIR / "templates" )

@app.get("/root")
async def root():
    return {"message": "Hello World"}

@app.get("/")
def home_view(request: Request):
    display_text = ""
    for i in range(1, 4):
        url = 'http://' + server_host + str(i) + ":" + str(server_port) + '/'
        try:
            x = requests.get(url)
            if x.status_code != 200:
                display_text += "server {} is not available right now\n".format(i) 
            else :
                display_text += x.json()["log"]
        except: 
            display_text += "server {} is dead\n".format(i)
    return templates.TemplateResponse("home.html", {"request": request, "display_text": display_text})

@app.post("/")
def home_signup_view(request: Request, server:str = Form(...), input_text:str = Form(...)):
    try:
        url = 'http://' + server_host + str(server) + ":" + str(server_port) + '/'
        requests.post(url, params={'s' : input_text})
    except:
        pass
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 3000, log_level="info")




