📌 Lab 1 – Deploy Nginx on Kubernetes
Steps & Commands
1️⃣ Start Minikube
'''bash
minikube start --driver=docker

2️⃣ Create Nginx Pod
kubectl run hello-k8s --image=nginx --port=80

3️⃣ Check Pod
kubectl get pods

4️⃣ Expose Pod
kubectl expose pod hello-k8s --type=NodePort --port=80

5️⃣ Access the App
minikube service hello-k8s


Or:

minikube service hello-k8s --url
