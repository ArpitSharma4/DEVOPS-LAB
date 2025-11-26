## 🧪 Lab 1 – Deploy Nginx on Kubernetes
### 📌 Steps & Commands  

---

### **1️⃣ Start Minikube**
```bash
minikube start --driver=docker
```

---

### **2️⃣ Create Nginx Pod**
```bash
kubectl run hello-k8s --image=nginx --port=80
```

---

### **3️⃣ Check Pod**
```bash
kubectl get pods
```

---

### **4️⃣ Expose Pod as NodePort**
```bash
kubectl expose pod hello-k8s --type=NodePort --port=80
```

---

### **5️⃣ Access the Application**
```bash
minikube service hello-k8s
```

OR

```bash
minikube service hello-k8s --url
```