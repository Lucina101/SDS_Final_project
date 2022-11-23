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
    url = 'http://' + server_host + ":" + server_port + '/'
    x = requests.get(url)

    if x.status_code != 200:
        display_text = "server is not available right now\n" 
    else :
        display_text = x.json()["log"]

    return templates.TemplateResponse("home.html", {"request": request, "display_text": display_text})

@app.post("/")
def home_signup_view(request: Request, server:str = Form(...), input_text:str = Form(...)):
    url = 'http://' + server_host + ":" + server_port + '/'
    x = requests.post(url, params={'s' : input_text})
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000, log_level="info")




