from fastapi import FastAPI
from basic_auth import router
from basic_auth_2 import router as router_2
from song_router import router as router_3
from instrument_router import router as router_4
from authorized_router import router as router_5


app = FastAPI()
app.include_router(router)
app.include_router(router_2)
app.include_router(router_3)
app.include_router(router_4)
app.include_router(router_5)

