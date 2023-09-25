import redis

REDIS_HOST = 'redis'
REDIS_PORT = 6379

r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
