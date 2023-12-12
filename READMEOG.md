# Secret (For Our App)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: redis-secret
  namespace: default
type: Opaque
```

# Configmap (For Our App)

```yaml
apiVersion: v1
data:
  REDIS_APPEND_RAND_MAX_NUMBER: "20"
  REDIS_APPEND_SLEEP_SECS: "2"
  REDIS_DELETE_CHANCE_EACH_LOOP: "20"
  REDIS_DELETE_RAND_MAX_NUMBER: "20"
  REDIS_HOST: 192.168.49.2 # eğer ip değişecekse makine ipsi değişmeyecekse 'localhost'
  REDIS_LIST_KEY: mylist
  REDIS_PORT: "31961" # redis servisinin portu
kind: ConfigMap
metadata:
  name: redis-configmap
  namespace: default
```

# Redis Simulator Deployment (For Our App)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-simulator
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis-simulator
  template:
    metadata:
      labels:
        app: redis-simulator
    spec:
      containers:
      - name: redis-simulator
        image: jrdeveloper06/redis-simulator:original # Redis pod olarak çalışacaksa uygulama içerisinden localhost ve port'u değiştiriyoruz
        command: ["python", "redis-client-simulator.py"]
        ports:
        - containerPort: 6379
        envFrom:
        - configMapRef:
            name: redis-configmap
        - secretRef:
            name: redis-secret
```


---

# Redis install

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis
        ports:
        - containerPort: 6379
```

# Redis service install

```yaml
apiVersion: v1
kind: Service
metadata:
  name: redis-service
  namespace: default
spec:
  ports:
  - port: 6379
    protocol: TCP
    targetPort: 6379
  selector:
    app: redis
  type: NodePort
```

---
# Install Keda And Redis-Server

```yaml
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
helm install keda kedacore/keda

sudo apt install redis-server
systemctl start redis-server
systemctl status redis-server
```

# ScaledObject 

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: nginx-scaledobject
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: nginx-deployment # Hangi uygulamayı autoscale etmek istiyorsan onun adı
  pollingInterval: 5
  cooldownPeriod: 300
  minReplicaCount: 1
  maxReplicaCount: 10
  triggers:
  - type: redis
    metadata:
      address: 192.168.49.2:31961 # Makine ip ise makine ip verip port yazıyoruz host:port şeklinde , port kısmına ise redisin nodeport'unu yazıyoruz
      listName: mylist
      listLength: "5"
      activationListLength: "5"
      enableTLS: "false"
      unsafeSsl: "false"
      databaseIndex: "0"
```

# For test nginx-deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
```