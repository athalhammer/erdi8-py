#!/usr/bin/env python3

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, BaseSettings
from pathlib import Path
from erdi8 import Erdi8

class IdModel(BaseModel):
    id: str

class Settings(BaseSettings):
    erdi8_seed: int
    erdi8_start: str
    erdi8_safe: bool
    erdi8_filename: str

    class Config:
        env_file = "fastid.env"

settings = Settings()
e8 = Erdi8(settings.erdi8_safe)
app = FastAPI()

Path(settings.erdi8_filename).touch(exist_ok=True)


@app.post("/", status_code=201, response_model=IdModel)
async def id_generator():
    old = settings.erdi8_start
    with open(settings.erdi8_filename, "r+") as f:
        try:
            tmp = f.readline().strip()
            if tmp != "":
                old = tmp
            if tmp == settings.erdi8_start:
                return JSONResponse(status_code=500, content={'reason': 'ran out of identifiers'})
        except:
            pass
        else:
            new = e8.increment_fancy(old, settings.erdi8_seed)
            f.seek(0)
            print(new, file=f)
            return {"id": new}
