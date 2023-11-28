import time
from ipaddress import ip_address
from typing import Callable
import redis.asyncio as redis
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import uvicorn
from contextlib import asynccontextmanager

from src.database.db import get_db
from src.routes import contacts, auth, users


app = FastAPI()

origins = [
    "http://192.0.0.2:8000"
]
banned_ips = [ip_address("192.168.1.1"), ip_address(
    "192.168.1.2")]

'''
app.on_event("startup")
async def startup():
    r = await redis.Redis(host='localhost', port=6379, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)
'''
@asynccontextmanager
async def lifespan(app: FastAPI):
    r = await redis.Redis(host='localhost', port=6379, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    #origins,
    #['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.middleware('http')
async def custom_middleware(request: Request, call_next):
    start_time = time.time()
    responce = await call_next(request)
    during = time.time() - start_time
    responce.headers['perfomance'] = str(during)
    return responce

'''
@app.middleware("http")
async def ban_ips(request: Request, call_next: Callable):
    ip = ip_address(request.client.host)
    if ip in banned_ips:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
    response = await call_next(request)
    return response
'''
@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)