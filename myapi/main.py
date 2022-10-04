from fastapi import FastAPI
from myapi.api import router

app = FastAPI()

app.include_router(router=router, prefix="")