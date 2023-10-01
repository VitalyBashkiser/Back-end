from decouple import config
import redis

REDIS_HOST = config('REDIS_HOST', default='redis')
REDIS_PORT = config('REDIS_PORT', default=6379, cast=int)

r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
