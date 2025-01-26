import redis
import os

class RedisService:
    def __init__(self):
        self.redis_client = redis.StrictRedis.from_url(
            redis_url = os.getenv("REDIS_URL"),
            decode_responses=True
        )

    def set_value(self, key, value, expiration=None):
        self.redis_client.set(key, value, ex=expiration)

    def get_value(self, key):
        return self.redis_client.get(key)

    def delete_value(self, key):
        self.redis_client.delete(key)
