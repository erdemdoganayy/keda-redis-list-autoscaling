# Keda Autoscaling With Redis

https://keda.sh/

KEDA is a Kubernetes Autoscaler that can listen to many sources of events. The number of messages in a queue or in a topic, redis list lengths, memory metrics and many more. 
It can also scale down to zero pods.

In this task we will setup a KEDA deployment that will listen to a Redis list length and scale up and down a deployment based on the number of elements in the list.

Our app is a redis client simulator that can append and delete elements from a Redis list depending on it's environment variable configuration.

## Task

You may use local clusters(minikube, kind etc.) for this task.

- [ ] Create a repo for this task (e.g. keda-redis-list-autoscaling)
- [ ] Create a Docker image (preferably multi-stage) for our app/
- [ ] Push the image to Docker Hub
- [ ] Create k8s deployment .yaml manifests for our app:
    - [ ] Secret (for the Redis password)
    - [ ] ConfigMap (for all of the Redis Env)
    - [ ] Deployment (must get it's env. var. configs from configmap and secret)
- [ ] Install Redis in the cluster
- [ ] Install KEDA in the cluster
- [ ] Create the necessary k8s configurations for Keda to:
    - [ ] autoscale the deployment based on the number of elements in the Redis list 
- [ ] Update the redis-client-simulator Pods config-map to simulate:
    - [ ] Increasing number of messages to scale up our Deployment 
    - [ ] Decrease the number of messages to scale down our Deployment
- [ ] have a readme.md file with all of the instructions and commands to run the task


> Note: I'll try to run your commands in your repo -- in the KodeKloud clusters to test it.

### Dependencies
```bash
pip3 install -r requirements.txt
```

### Local Redis Setup
```bash
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest  

redis-cli -h localhost
# inside the redis-cli you can run the following commands
    KEYS *
    LRANGE mylist 0 -1
```


### Environment Variables

| Env. Var. Name | Default Value | Description |
|--------------|---------------|-------------|
| REDIS_HOST | "localhost" | The Redis server hostname |
| REDIS_PORT | 6379 | The Redis server port |
| REDIS_PASSWORD | None | The Redis server password |
| REDIS_LIST_KEY | "mylist" | The Redis list key to use |
| REDIS_APPEND_RAND_MAX_NUMBER | 20 | The Ceiling Random (1-N) number of elements to append to the Redis list |
| REDIS_APPEND_SLEEP_SECS | 20 | The number of seconds to sleep between Redis operations |
| REDIS_DELETE_RAND_MAX_NUMBER | 20 | The maximum number of elements to delete from the Redis list |
| REDIS_DELETE_CHANCE_EACH_LOOP | 20 | The chance (in percentage) to delete a random amount of items from the Redis list on each loop |

```bash
export REDIS_HOST=localhost
export REDIS_PORT=6379
# export REDIS_PASSWORD=
export REDIS_LIST_KEY=mylist
export REDIS_APPEND_RAND_MAX_NUMBER=20
export REDIS_APPEND_SLEEP_SECS=20
export REDIS_DELETE_RAND_MAX_NUMBER=20
export REDIS_DELETE_CHANCE_EACH_LOOP=20 # make it 100 to delete on each loop
```