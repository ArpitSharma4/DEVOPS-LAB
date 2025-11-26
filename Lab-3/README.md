## 🧪 Lab 3 – Scale Flask Flash Sale App Using ReplicaSets  
### 📌 Steps & Commands  

---

### **1️⃣ Create Flask Flash Sale Application (`app.py`)**
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
```

---

### **2️⃣ Create Dockerfile**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir flask gunicorn
CMD ["gunicorn","-b","0.0.0.0:5000","app:app","--workers","1","--threads","2"]
```

---

### **3️⃣ Create ReplicaSet + Service (`flashsale-replicaset.yaml`)**
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
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "256Mi"
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
```

---

### **4️⃣ Start Minikube**
```bash
minikube start --nodes=1
```

---

### **5️⃣ (Optional) Clean Previous Minikube**
```bash
minikube stop
minikube delete
```

---

### **6️⃣ Build Image Inside Minikube (if not using DockerHub)**
```powershell
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
```

Build image:
```bash
docker build -t flashsale:1.0 .
```

---

### **7️⃣ Deploy ReplicaSet + Service**
```bash
kubectl apply -f flashsale-replicaset.yaml
```

---

### **8️⃣ Check ReplicaSet**
```bash
kubectl get rs
```

---

### **9️⃣ Check Pods**
```bash
kubectl get pods -l app=flashsale
```

---

### **🔟 Forward Port and Access the App**
```bash
kubectl port-forward svc/flashsale-svc 8000:80
```

Open in browser:
```
http://localhost:8000/
```

Test Flash Sale endpoint:
```bash
curl http://localhost:8000/buy?user=arpit
```

---

### **1️⃣1️⃣ Scale the ReplicaSet**
```bash
kubectl scale rs flashsale-rs --replicas=5
```

---

### **1️⃣2️⃣ Verify Scaling**
```bash
kubectl get pods -l app=flashsale
kubectl get rs
kubectl get pods -o wide
```

---

### **1️⃣3️⃣ Test Self-Healing (Delete a Pod)**
```bash
kubectl delete pod <pod-name>
```

Check new pod created:
```bash
kubectl get pods -l app=flashsale
```

---

### **1️⃣4️⃣ Cleanup (Optional)**
```bash
kubectl delete -f flashsale-replicaset.yaml
minikube stop
```

---
