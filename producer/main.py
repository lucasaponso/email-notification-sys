from fastapi import FastAPI
from pydantic import BaseModel
import routes.mq as mq

app = FastAPI()

app.include_router(mq.router)

@app.get("/")
def welcome():
    return "HELLWOROLD"