from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here

    class Config:
        priority = 997