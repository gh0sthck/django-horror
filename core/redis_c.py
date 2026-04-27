import os

from dotenv import load_dotenv
import redis

load_dotenv()


REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")


def get_redis_connection() -> redis.Redis | None:
    try:
        conn = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT
        )
    except redis.ConnectionError as e:
        print(f"[REDIS ERROR] {e}")
        conn = None
    return conn
