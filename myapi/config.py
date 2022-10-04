from pydantic import BaseConfig

class Config(BaseConfig):
    database_url: str

    class Config:
        env_file = ".env"

config = Config()