from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from myapi.api import router
from myapi.config import settings

app = FastAPI()
app.mount("/storage", StaticFiles(directory=settings.storage_dir), name="storage")

app.include_router(router=router, prefix="")
