## 🧪 Lab 4 – Docker Networking with Multiple Containers  
### 📌 Steps & Commands  

---

### **1️⃣ Create a Custom Bridge Network**
```bash
docker network create --driver bridge my-bridge-net
```

---

### **2️⃣ Verify the Network**
```bash
docker network ls
```

---

### **3️⃣ Inspect the Network**
```bash
docker network inspect my-bridge-net
```

---

### **4️⃣ Create Flask Application (`app.py`)**
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/about', methods=['GET'])
def about():
    return jsonify({
        "name": "Simple REST API",
        "version": "1.0",
        "description": "This is a simple REST API built with Flask."
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5001)
```

---

### **5️⃣ Create Requirements File (`requirements.txt`)**
```
Flask==2.2.5
Werkzeug==2.2.3
```

---

### **6️⃣ Create Dockerfile**
```dockerfile
FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt .
COPY app.py .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "app.py"]
```

---

### **7️⃣ Build the Flask Image**
```bash
docker build -t flask-api .
```

---

### **8️⃣ Run MySQL, Redis & Flask Containers on the Same Network**
```bash
docker run -d --name mysql --net=my-bridge-net -e MYSQL_ROOT_PASSWORD=root mysql:latest
docker run -d --name redis --net=my-bridge-net redis:latest
docker run -d --name flask --net=my-bridge-net -p 5001:5001 flask-api
```

---

### **9️⃣ Test Flask API (Host Machine)**
```bash
curl http://localhost:5001/about
```

Expected output:
```json
{
  "name": "Simple REST API",
  "version": "1.0",
  "description": "This is a simple REST API built with Flask."
}
```

---

### **🔟 Test Container Connectivity**

#### Enter Flask Container:
```bash
docker exec -it flask bash
```

#### Ping Redis:
```bash
ping -c 1 redis
```

#### Ping MySQL:
```bash
ping -c 1 mysql
```

---

### **1️⃣1️⃣ Optional: Check Docker DNS**
```bash
getent hosts mysql
getent hosts redis
```

---

### **1️⃣2️⃣ Optional: Test Port (if netcat installed)**
```bash
nc -zv mysql 3306
```

---

### **1️⃣3️⃣ Cleanup**
```bash
docker stop mysql redis flask
docker rm mysql redis flask
docker network rm my-bridge-net
```

---
