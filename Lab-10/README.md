# Multi-Node Kubernetes Cluster for Product Catalog & Shopping Cart  
# (Windows + VS Code + Minikube + Docker Driver)  
---

# 0️⃣ CLEAN UP EXISTING MINIKUBE
---
Open **WSL Ubuntu** (NOT PowerShell) and run:
minikube stop
minikube delete

# 1️⃣ START MULTI-NODE MINIKUBE CLUSTER (3 NODES)
---
Run in **WSL Ubuntu**:
minikube start --nodes 3 -p devops-multinode --force

Enable registry addon:
minikube -p devops-multinode addons enable registry

# 2️⃣ CREATE APPLICATION FILES IN WINDOWS + VS CODE
---
Inside a folder (example: C:\DEV-1\Lab-10) create:

## product_catalog.py
from flask import Flask, jsonify

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Phone", "price": 800},
    {"id": 3, "name": "Headphones", "price": 150},
]

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

## shopping_cart.py
from flask import Flask, jsonify, request

app = Flask(__name__)

cart = []

@app.route("/cart", methods=["GET"])
def get_cart():
    return jsonify(cart)

@app.route("/cart", methods=["POST"])
def add_to_cart():
    item = request.json
    cart.append(item)
    return jsonify(cart), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

# 3️⃣ DOCKERIZE BOTH APPS (WINDOWS POWERSHELL)
---
Open **PowerShell** in project folder:

## Dockerfile.product
FROM python:3.9-slim
WORKDIR /app
COPY product_catalog.py /app/
RUN pip install flask
CMD ["python", "product_catalog.py"]

## Dockerfile.shopping
FROM python:3.9-slim
WORKDIR /app
COPY shopping_cart.py /app/
RUN pip install flask
CMD ["python", "shopping_cart.py"]

Build images:
docker build -t product-catalog:latest -f Dockerfile.product .
docker build -t shopping-cart:latest -f Dockerfile.shopping .

List images:
docker images

# 4️⃣ LOAD IMAGES INTO MINIKUBE REGISTRY (WSL UBUNTU ONLY)
---
minikube -p devops-multinode image load product-catalog:latest
minikube -p devops-multinode image load shopping-cart:latest

Verify:
minikube -p devops-multinode ssh -- docker images

# 5️⃣ CREATE DEPLOYMENTS (WINDOWS)
---
Create YAML files in VS Code.

## product_catalog_deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-catalog
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: product-catalog
  template:
    metadata:
      labels:
        app: product-catalog
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: product-catalog
            topologyKey: "kubernetes.io/hostname"
      containers:
      - name: product-catalog-container
        image: product-catalog:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 80

## shopping_cart_deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: shopping-cart
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: shopping-cart
  template:
    metadata:
      labels:
        app: shopping-cart
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: shopping-cart
            topologyKey: "kubernetes.io/hostname"
      containers:
      - name: shopping-cart-container
        image: shopping-cart:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 80

Apply (in PowerShell):
kubectl apply -f product_catalog_deployment.yaml
kubectl apply -f shopping_cart_deployment.yaml

# 6️⃣ CREATE SERVICES
---
## product_catalog_service.yaml
apiVersion: v1
kind: Service
metadata:
  name: product-catalog-service
  namespace: default
spec:
  selector:
    app: product-catalog
  ports:
  - port: 80
    targetPort: 80
  type: NodePort

## shopping_cart_service.yaml
apiVersion: v1
kind: Service
metadata:
  name: shopping-cart-service
  namespace: default
spec:
  selector:
    app: shopping-cart
  ports:
  - port: 80
    targetPort: 80
  type: NodePort

Apply:
kubectl apply -f product_catalog_service.yaml
kubectl apply -f shopping_cart_service.yaml

# 7️⃣ VERIFY POD DISTRIBUTION
---
kubectl get pods -o wide

Expected:
- 2 Product Catalog pods across different nodes
- 3 Shopping Cart pods across all nodes

# 8️⃣ ACCESS SERVICES (WINDOWS)
---
DO NOT USE auto-open tunnel.  
USE THIS COMMAND:

## Product Catalog URL
minikube -p devops-multinode service product-catalog-service --url

Open in browser:
http://192.168.49.2:<nodeport>/products

## Shopping Cart URL
minikube -p devops-multinode service shopping-cart-service --url

Open:
http://192.168.49.2:<nodeport>/cart

# 9️⃣ TEST USING POWERSHELL COMMANDS
---
## GET PRODUCTS
Invoke-WebRequest -Uri "http://127.0.0.1:<port>/products" -Method GET

## GET CART
Invoke-WebRequest -Uri "http://127.0.0.1:<port>/cart" -Method GET

## POST ADD TO CART
Invoke-WebRequest -Uri "http://127.0.0.1:<port>/cart" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"id":1,"name":"Laptop","quantity":1}'

Refresh cart:
Invoke-WebRequest -Uri "http://127.0.0.1:<port>/cart" -Method GET

# 🔟 SUMMARY
---
✔ Multi-node Minikube cluster (3 nodes)  
✔ Product Catalog (GET /products)  
✔ Shopping Cart (GET + POST /cart)  
✔ Anti-affinity scheduling across nodes  
✔ Docker images loaded into Minikube registry  
✔ NodePort services working  
✔ Windows-friendly commands provided

# ✅ END OF README
---
