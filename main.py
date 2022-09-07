import os
from typing import Union
from fastapi import FastAPI, Request, Header, HTTPException, status
from pydantic import BaseModel, parse_obj_as
from passlib.context import CryptContext
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

myctx = CryptContext(schemes="md5_crypt")
DATASEFDF = os.environ.get("DATASEFDF")
USDRMONG = os.environ.get("USDRMONG")

client = MongoClient(
    USDRMONG)
db = client.nivedcs


@app.get("/procesos")
def read_procesos(tracss: Union[str, None] = Header(default=None)):
    if not (myctx.verify(tracss, DATASEFDF)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return [x for x in db.proceso.find({}, {"_id": 0, "id": 1, "entidad": 1,
                                            "tipo": 1, "valor": 1, "objeto": 1, "link": 1, "estado": 1, "detalle": 1})]


@app.get("/pendientes")
def read_pendientes(tracss: Union[str, None] = Header(default=None)):
    if not (myctx.verify(tracss, DATASEFDF)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return [x for x in db.pendiente.find({}, {"_id": 0, "id": 1, "tarea": 1,
                                              "estado": 1, "idproceso": 1})]


@app.get("/eventos")
async def read_eventos(tracss: Union[str, None] = Header(default=None)):
    if not (myctx.verify(tracss, DATASEFDF)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # return parse_obj_as(List[Evento], [x for x in db.evento.find({}, {"_id": 0, "id": 1, "evento": 1})])
    return [x for x in db.evento.find({}, {"_id": 0, "id": 1, "evento": 1})]



