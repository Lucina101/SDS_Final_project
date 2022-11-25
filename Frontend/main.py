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
    query_str = ['average', 'maximum']
    for i in range(2, 4):
        url = 'http://' + server_host + ("" if server_host == 'localhost' else str(i)) + ":" + str(int(server_port) + i - 1) + '/'
        try:
            x = requests.get(url)
            if x.status_code == 200:
                display_text += "{} value = {:.5f}\n".format(query_str[i - 2] ,x.json()[query_str[i - 2]]) 
            elif x.status_code == 400:
                display_text += "No data in db right now\n"
            else:
                display_text += "server {} is not working right\n".format(i)
        except: 
            display_text += "server {} is dead\n".format(i)
    return templates.TemplateResponse("home.html", {"request": request, "display_text": display_text})

@app.post("/")
def home_signup_view(request: Request, server:str = Form(...), input_text:str = Form(...)):
    try:
        url = 'http://' + server_host  + ("" if server_host == 'localhost' else "1")+ ":" + str(server_port) + '/'
        requests.post(url, params={'x' : input_text})
    except:
        pass
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port = 3000, log_level="info")




