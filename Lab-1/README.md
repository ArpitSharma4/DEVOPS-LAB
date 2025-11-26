# 🚀 Lab 2: Deploy a Flask App Using Docker + YAML
### 📝 Description

This lab teaches how to deploy your own Python Flask application on Kubernetes.
You will:

Build a Docker image

Configure Minikube’s Docker environment

Deploy using a Kubernetes Deployment manifest

Expose the app using a Service

Access the Flask API in your browser

## 📂 Project Structure
flask-k8s/
│
├── app.py
├── Dockerfile
└── flask-deployment.yaml

## 📄 Files
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

## 🧪 Steps & Commands
### 1️⃣ Start Minikube
minikube start --driver=docker

### 2️⃣ Point Docker CLI to Minikube’s Docker Daemon

This ensures images are built inside Minikube so Kubernetes can access them.

& minikube -p minikube docker-env --shell powershell | Invoke-Expression


Verify:

docker info

### 3️⃣ Build the Flask Docker Image

Run this inside the folder containing Dockerfile and app.py:

docker build -t flask-app:latest .

### 4️⃣ Deploy Flask App to Kubernetes
kubectl apply -f flask-deployment.yaml

### 5️⃣ Verify Deployment & Pods
kubectl get deployments
kubectl get pods -l app=flask-app

### 6️⃣ View Pod Logs
kubectl logs <pod-name>


Expected:

Running on http://0.0.0.0:15000

### 7️⃣ Access the Flask Application

Get service URL:

minikube service flask-app-service --url


Example:

http://127.0.0.1:36157


Open in browser → You should see:

Hello from Flask on Kubernetes!
