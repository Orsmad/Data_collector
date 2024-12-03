import os
from dotenv import load_dotenv

from config.logger import logger


class Config:
    """Class to hold the application settings."""

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_REGION")
    SHARD_SIZE = int(os.getenv("SHARD_SIZE"))
    MAX_WORKERS = int(os.getenv("MAX_WORKERS"))


def load_env_vars():
    logger.debug(f"Loading env vars")
    load_dotenv()


load_env_vars()

config = Config()
