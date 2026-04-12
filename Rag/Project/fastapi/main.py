from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette import status
from fastapi.staticfiles import StaticFiles
from router import main

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def root_redirect(request: Request):
    return RedirectResponse(url="/AskMe/", status_code=status.HTTP_302_FOUND)

app.include_router(main.router)

