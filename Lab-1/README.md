📘 Kubernetes Labs – Nginx Pod + Flask App Deployment

This repository contains two Kubernetes hands-on labs designed to help you understand how to deploy containerized applications on a local Kubernetes cluster using Minikube.

## 🚀 Lab 1: Deploy Nginx as a Pod (Hello Pod Exercise)
### 📝 Description

This lab teaches the basics of Kubernetes by deploying an Nginx container as a Pod and exposing it using a Service. You will learn how to start Minikube, create Pods, expose Services, and access applications running inside the cluster.

### 📂 Files Used

(No files required — all commands executed via terminal)

### 🧪 Steps & Commands
1️⃣ Start Minikube
minikube start --driver=docker

2️⃣ Create an Nginx Pod
kubectl run hello-k8s --image=nginx --port=80

3️⃣ Verify Pod Status
kubectl get pods


Expected:

hello-k8s   1/1   Running

4️⃣ Expose Pod as a Service (NodePort)
kubectl expose pod hello-k8s --type=NodePort --port=80

5️⃣ List Services
kubectl get svc

6️⃣ Access the Nginx Application
minikube service hello-k8s


If the browser does not open, use:

minikube service hello-k8s --url


Paste URL in your browser → You should see the Nginx welcome page.
