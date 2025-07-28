import redis

r = redis.StrictRedis(
    host='redis-13625.c258.us-east-1-4.ec2.redns.redis-cloud.com',
    port=13625,
    password='Q25rFLLivgM1Nr1pNE4IZjJk6t7G8p8k',
    decode_responses=True
)
print("Connected to Redis:", r.ping())
