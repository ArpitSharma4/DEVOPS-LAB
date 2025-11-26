## 🧪 Lab 2 – Deploy Flask App on Kubernetes  
### 📌 Steps & Commands  

---

### **1️⃣ Create Flask Application (`app.py`)**
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask on Kubernetes!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000)
```

---

### **2️⃣ Create Dockerfile**
```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install flask
CMD ["python", "app.py"]
```

---

### **3️⃣ Create Kubernetes Deployment File (`flask-deployment.yaml`)**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
      - name: flask-app
        image: flask-app:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 15000
---
apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
spec:
  selector:
    app: flask-app
  ports:
  - port: 15000
    targetPort: 15000
  type: NodePort
```

---

### **4️⃣ Start Minikube**
```bash
minikube start --driver=docker
```

---

### **5️⃣ Configure Docker to Use Minikube**
```powershell
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
```

Verify:
```bash
docker info
```

---

### **6️⃣ Build Docker Image**
```bash
docker build -t flask-app:latest .
```

---

### **7️⃣ Deploy to Kubernetes**
```bash
kubectl apply -f flask-deployment.yaml
```

---

### **8️⃣ Check Deployment**
```bash
kubectl get deployments
```

---

### **9️⃣ Check Pods**
```bash
kubectl get pods -l app=flask-app
```

---

### **🔟 Access the App**
```bash
minikube service flask-app-service --url
```

Example output:
```
http://127.0.0.1:36157
```

Test:
```bash
curl http://127.0.0.1:36157
```

You should see:
```
Hello from Flask on Kubernetes!
```

---
