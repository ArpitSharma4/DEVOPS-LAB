# ✅ LAB 1 – Deploy Nginx on Kubernetes
📌 Step 1 — Start Minikube
using
minikube start --driver=docker

📌 Step 2 — Create Nginx Pod
using
kubectl run hello-k8s --image=nginx --port=80

📌 Step 3 — Check Pod Status
using
kubectl get pods

📌 Step 4 — Expose Pod as NodePort
using
kubectl expose pod hello-k8s --type=NodePort --port=80

📌 Step 5 — Check Services
using
kubectl get svc

📌 Step 6 — Access the App

Auto-open:

minikube service hello-k8s


Or get URL manually:

minikube service hello-k8s --url


Paste URL in browser → Nginx welcome page.