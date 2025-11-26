# ✅ LAB 2 – Deploy Flask App on Kubernetes
📌 Step 0 — Files Needed

Create these inside one folder:

app.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask on Kubernetes!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000)

Dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install flask
CMD ["python", "app.py"]

flask-deployment.yaml
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

# 🚀 Execution Steps & Commands
📌 Step 1 — Start Minikube
minikube start --driver=docker

📌 Step 2 — Use Minikube’s Docker Daemon
& minikube -p minikube docker-env --shell powershell | Invoke-Expression


Verify:

docker info

📌 Step 3 — Build Flask Docker Image
docker build -t flask-app:latest .

📌 Step 4 — Deploy Flask App
kubectl apply -f flask-deployment.yaml

📌 Step 5 — Check Deployment
kubectl get deployments

📌 Step 6 — Check Pods
kubectl get pods -l app=flask-app

📌 Step 7 — View Logs (Optional)
kubectl logs <pod-name>

📌 Step 8 — Access the Flask App

Get external URL:

minikube service flask-app-service --url


Example output:

http://127.0.0.1:36157


Test using curl:

curl http://127.0.0.1:36157


Or open the URL in your browser →
You should see:

Hello from Flask on Kubernetes!