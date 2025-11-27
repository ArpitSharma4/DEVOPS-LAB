# Docker Security with AppArmor and Python  
### Complete Ubuntu Guide – Build, Apply, Test AppArmor Profile for a Flask App

---

# 1️⃣ Objective
Secure a Dockerized Python Flask app using an **AppArmor profile**, apply it to Docker, verify confinement, and automate tests using the **Docker SDK for Python**.

---

# 2️⃣ Prerequisites (Ubuntu)

### Update & install required packages:
```bash
sudo apt update
sudo apt install -y docker.io apparmor apparmor-utils python3-pip
```

### Start & enable Docker:
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### Check AppArmor status:
```bash
sudo aa-status
```

### Install Python Docker SDK:
```bash
pip3 install --user docker
```

---

# 3️⃣ Project Setup

### Create working directory:
```bash
mkdir ~/flask-secure && cd ~/flask-secure
```

### Create `app.py`
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is a secure Flask application running inside a Docker container!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Create `Dockerfile`
```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir flask
EXPOSE 5000
CMD ["python", "app.py"]
```

---

# 4️⃣ Build Docker Image

```bash
sudo docker build -t flask-apparmor .
sudo docker images | grep flask-apparmor
```

---

# 5️⃣ Create AppArmor Profile (Secure)

Open profile file:
```bash
sudo nano /etc/apparmor.d/my-apparmor-profile
```

Paste the profile:
```text
#include <tunables/global>
profile my-apparmor-profile flags=(attach_disconnected) {

  deny /etc/** rwmklx,
  deny /var/** rwmklx,

  deny /bin/sh x,
  deny /usr/bin/sh x,
  deny /bin/dash x,
  deny /usr/bin/dash x,
  deny /bin/bash x,
  deny /usr/bin/bash x,

  /usr/local/bin/python rix,
  /usr/local/bin/python3 rix,
  /usr/local/bin/python3.8 rix,

  /usr/local/lib/** mr,
  /usr/lib/** mr,
  /lib/** mr,
  /lib64/** mr,

  /etc/ld.so.cache r,
  /etc/hosts r,
  /etc/resolv.conf r,
  /proc/** r,
  /sys/** r,

  network inet stream,

  /app/** rwk,

  capability net_bind_service,
  deny capability sys_admin,
}
```

---

# 6️⃣ Load & Enforce Profile

Reload:
```bash
sudo apparmor_parser -r /etc/apparmor.d/my-apparmor-profile
```

Enforce:
```bash
sudo aa-enforce /etc/apparmor.d/my-apparmor-profile
```

Verify:
```bash
sudo aa-status | grep my-apparmor-profile
```

If profile is inside *disable*:
```bash
sudo mv /etc/apparmor.d/disable/my-apparmor-profile /etc/apparmor.d/
```

---

# 7️⃣ Run Flask Container Under AppArmor

Start container:
```bash
sudo docker run --security-opt apparmor=my-apparmor-profile \
 -p 5000:5000 --name flask-secure-instance -d flask-apparmor
```

Check status:
```bash
sudo docker ps
```

Access app:
```bash
curl http://localhost:5000
```

---

# 8️⃣ Manual Security Tests

### 1. Attempt to read `/etc/passwd`
```bash
sudo docker exec -it flask-secure-instance cat /etc/passwd
```

Expected: **Permission denied**

---

### 2. Attempt to spawn a shell
```bash
sudo docker exec -it flask-secure-instance /bin/sh
```

Expected: **Permission denied or command not found**

---

### 3. Attempt to write to `/var`
```bash
sudo docker exec -it flask-secure-instance sh -c "echo hi > /var/test"
```

Expected: **Permission denied**

---

### 4. If container fails to stop:
```bash
sudo docker kill flask-secure-instance
sudo docker rm flask-secure-instance
```

---

# 9️⃣ Python Automation (Docker SDK)

## 9.1 Install SDK
```bash
pip3 install --user docker
```

---

## 9.2 `apply_apparmor.py`

```python
import docker
import sys

client = docker.from_env()

print("Building image...")
image, logs = client.images.build(path='.', tag='flask-apparmor')

for chunk in logs:
    if 'stream' in chunk:
        sys.stdout.write(chunk['stream'])

print("Running container with AppArmor profile...")
container = client.containers.run(
    "flask-apparmor",
    ports={'5000/tcp': 5000},
    security_opt=["apparmor=my-apparmor-profile"],
    detach=True,
    name="flask-secure-auto"
)

print("Container started:", container.short_id)

info = client.api.inspect_container(container.id)
print("HostConfig.SecurityOpt:", info.get('HostConfig', {}).get('SecurityOpt'))

container.stop()
container.remove()
```

Run:
```bash
python3 apply_apparmor.py
```

Expected:
- Build logs printed  
- Container started  
- `SecurityOpt` contains `apparmor=my-apparmor-profile`

---

## 9.3 `test_restricted_actions.py`

```python
import docker, time

client = docker.from_env()

container = client.containers.run(
    "flask-apparmor",
    ports={'5000/tcp': 5000},
    security_opt=["apparmor=my-apparmor-profile"],
    detach=True,
    name="flask-secure-test"
)

time.sleep(1)

code, out = container.exec_run("cat /etc/passwd")
print("Read /etc/passwd:", code, out.decode(errors='replace'))

code, out = container.exec_run("/bin/sh -c 'echo shell-up'")
print("Execute /bin/sh:", code, out.decode(errors='replace'))

container.stop()
container.remove()
```

Run:
```bash
python3 test_restricted_actions.py
```

Expected:
- `/etc/passwd` read → non-zero exit code  
- Shell execution → **denied**

---

# 🔟 Cleanup & Notes

Stop/remove containers:
```bash
sudo docker stop <container>
sudo docker rm <container>
```

Disable AppArmor profile:
```bash
sudo aa-disable /etc/apparmor.d/my-apparmor-profile
sudo apparmor_parser -R /etc/apparmor.d/my-apparmor-profile
```

Debug AppArmor:
```bash
sudo journalctl -k | grep -i apparmor
sudo dmesg | grep -i apparmor
```

Use complain mode while tuning:
```bash
sudo aa-complain /etc/apparmor.d/my-apparmor-profile
```

---

# 1️⃣1️⃣ Final Tips
- Make sure profile name matches the value passed to Docker.  
- Use **named profiles**, not binary-attached profiles.  
- Use **complain mode** to learn required permissions first, then enforce.  

---

# ✅ End of README
