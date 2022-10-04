import imp
from sqlmodel import Session, create_engine

from myapi.config import settings

engine = create_engine(settings.database_url)

def get_session():
    with Session(engine) as session:
        yield session