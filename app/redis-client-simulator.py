import redis
import logging
import time
import random
import string
import os
logging.basicConfig()
logger = logging.getLogger("redis-client-simulator")
logger.setLevel(logging.DEBUG)


def update_redis_list(redis_conn, key):
    # Generate random 4 char string
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    # Append random string to Redis list
    try:
        redis_conn.rpush(key, random_string)
        logger.info(f"Random string {random_string} appended to Redis list {key}")
    except redis.RedisError as e:
        logger.error(f"Error writing to Redis: {e}")


def remove_n_elements_from_redis_list(redis_conn, key, n):
    try:
        redis_conn.ltrim(key, n, -1)
        logger.info(f"{n} elements removed from Redis list {key}")
    except redis.RedisError as e:
        logger.error(f"Error removing elements from Redis: {e}")

def main(host, port, password, redis_list_key):
    try:
        r = redis.Redis(host=host, port=port, password=password)
        logger.info(f"Redis connection established at: {host}.")
    except redis.ConnectionError as e:
        logger.error(f"Could not connect to Redis: {e}")
        exit(-1)
    
    logger.info(f"Program will constantly update the Redis List Key: {redis_list_key}")
    

    redis_append_rand_max_number = int(os.environ.get("REDIS_APPEND_RAND_MAX_NUMBER", 20))
    redis_append_sleep_secs = int(os.environ.get("REDIS_APPEND_SLEEP_SECS", 20))
    redis_delete_rand_max_number = int(os.environ.get("REDIS_DELETE_RAND_MAX_NUMBER", 20))
    redis_delete_chance_each_loop = int(os.environ.get("REDIS_DELETE_CHANCE_EACH_LOOP", 20))

    # Log the values of the environment variables
    logger.info(f"Env Var Read: REDIS_APPEND_RAND_MAX_NUMBER= {redis_append_rand_max_number}")
    logger.info(f"Env Var Read: REDIS_APPEND_SLEEP_SECS= {redis_append_sleep_secs}")
    logger.info(f"Env Var Read: REDIS_DELETE_RAND_MAX_NUMBER= {redis_delete_rand_max_number}")
    logger.info(f"Env Var Read: REDIS_DELETE_CHANCE_EACH_LOOP= {redis_delete_chance_each_loop}")
    
    logger.info(f"Starting the main infinite loop...")
    while True:
        num_calls = random.randint(1, redis_append_rand_max_number)
        logger.info(f"{redis_list_key} list-key will be appended {num_calls} elements")
        for i in range(num_calls):
            update_redis_list(r, redis_list_key)
            
        logger.info(f"Sleeping for {redis_append_sleep_secs} seconds...")
        time.sleep(redis_append_sleep_secs)
        
        if random.randint(0, 100) <= redis_delete_chance_each_loop:
            delete_n_count =  random.randint(1, redis_delete_rand_max_number)
            logger.info(f"{redis_list_key} list-key will have {delete_n_count} elements removed")
            remove_n_elements_from_redis_list(r, redis_list_key, delete_n_count)

        

if __name__ == "__main__":
    redis_host = os.environ.get("REDIS_HOST", "localhost")
    redis_port = int(os.environ.get("REDIS_PORT", 6379))
    redis_password = os.environ.get("REDIS_PASSWORD", None)
    redis_list_key = os.environ.get("REDIS_LIST_KEY", "mylist")
    logger.info(f"Starting the Redis Simulator...")
    main(redis_host, redis_port, redis_password, redis_list_key)