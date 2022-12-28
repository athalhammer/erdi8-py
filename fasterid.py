#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, BaseSettings
from pathlib import Path
from erdi8 import Erdi8

class IdModel(BaseModel):
    id: str

class ErrorModel(BaseModel):
    detail: str

class Settings(BaseSettings):
    erdi8_seed: int
    erdi8_start: str
    erdi8_safe: bool
    erdi8_filename: str

    class Config:
        env_file = "fasterid.env"

settings = Settings()
e8 = Erdi8(settings.erdi8_safe)
app = FastAPI()

Path(settings.erdi8_filename).touch(exist_ok=True)

@app.post("/", status_code=201, responses={201: {"model": IdModel}, 500: {"model": ErrorModel}})
async def id_generator():
    old = settings.erdi8_start
    with open(settings.erdi8_filename, "r+") as f:
        tmp = f.readline().strip()
        if tmp != "":
            old = tmp
        if tmp == settings.erdi8_start:
            raise HTTPException(500, detail="🤷 ran out of identifiers")
        else:
            try:
                new = e8.increment_fancy(old, settings.erdi8_seed)
            except Exception as e:
                raise HTTPException(500, detail=getattr(e, 'message', repr(e)))
            f.seek(0)
            print(new, file=f)
            return {"id": new}
