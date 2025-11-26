## 🧪 Lab 3 – Scale Flask Flash Sale App Using ReplicaSets  
### 📌 Steps & Commands  

---

### 1️⃣ Create Flask Flash Sale Application (app.py)
```python
from flask import Flask, request
import socket, time, random

app = Flask(__name__)

@app.get("/")
def homepage():
    return {
        "message": "Welcome to Big Sale!",
        "pod": socket.gethostname(),
        "ts": time.time()
    }

@app.get("/buy")
def buy():
    item = random.choice(["Smartphone", "Shoes", "Headphones", "Laptop"])
    user = request.args.get("user", f"user{random.randint(1,1000)}")
    return {
        "status": "success",
        "item": item,
        "user": user,
        "served_by_pod": socket.gethostname(),
        "time": time.strftime("%H:%M:%S")
    }

@app.get("/health")
def health():
    return {"status": "healthy", "pod": socket.gethostname()}

---

### 2️⃣ Create Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir flask gunicorn
CMD ["gunicorn","-b","0.0.0.0:5000","app:app","--workers","1","--threads","2"]

---

### 3️⃣ Create ReplicaSet + Service (flashsale-replicaset.yaml)
```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: flashsale-rs
  labels:
    app: flashsale
spec:
  replicas: 3
  selector:
    matchLabels:
      app: flashsale
  template:
    metadata:
      labels:
        app: flashsale
    spec:
      containers:
      - name: flashsale-container
        image: flashsale:1.0
        ports:
        - containerPort: 5000
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 2
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: flashsale-svc
spec:
  selector:
    app: flashsale
  ports:
  - name: http
    port: 80
    targetPort: 5000
  type: ClusterIP

---

### 4️⃣ Start Minikube
minikube start --nodes=1

---

### 5️⃣ (Optional) Clean Previous Minikube
minikube stop
minikube delete

---

### 6️⃣ If NOT using DockerHub — Build Image Inside Minikube
Windows PowerShell:
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

Build:
docker build -t flashsale:1.0 .

---

### 7️⃣ Deploy ReplicaSet + Service
kubectl apply -f flashsale-replicaset.yaml

---

### 8️⃣ Check ReplicaSet
kubectl get rs

---

### 9️⃣ Check Pods
kubectl get pods -l app=flashsale

---

### 🔟 Access the Application
kubectl port-forward svc/flashsale-svc 8000:80

Browser:
http://localhost:8000/

Test:
curl http://localhost:8000/buy?user=arpit

---

### 1️⃣1️⃣ Scale the ReplicaSet
kubectl scale rs flashsale-rs --replicas=5

---

### 1️⃣2️⃣ Verify Scaling
kubectl get pods -l app=flashsale
kubectl get rs
kubectl get pods -o wide

---

### 1️⃣3️⃣ Test Self-Healing (Delete a Pod)
kubectl delete pod <pod-name>

Verify:
kubectl get pods -l app=flashsale

---

### 1️⃣4️⃣ Cleanup (Optional)
kubectl delete -f flashsale-replicaset.yaml
minikube stop

