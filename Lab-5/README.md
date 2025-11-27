# Docker Security with AppArmor and Python
### Complete Ubuntu Guide – Build, Apply, Test AppArmor Profile for a Flask App
---
# 1 Objective
Secure a Dockerized Python Flask app using an AppArmor profile; apply the profile with Docker, verify confinement, and automate tests with the Docker SDK for Python.

---
# 2 Prerequisites (Ubuntu)
1. Update & install packages:
   sudo apt update
   sudo apt install -y docker.io apparmor apparmor-utils python3-pip

2. Start & enable Docker:
   sudo systemctl start docker
   sudo systemctl enable docker

3. Check AppArmor:
   sudo aa-status

4. Install Python Docker SDK (host):
   pip3 install --user docker

---
# 3 Project setup
1. Create working directory:
   mkdir ~/flask-secure && cd ~/flask-secure

2. Create Flask app file (app.py) — paste and save:
   from flask import Flask
   app = Flask(__name__)
   @app.route('/')
   def home():
       return "Hello, this is a secure Flask application running inside a Docker container!"
   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)

3. Create Dockerfile — paste and save:
   FROM python:3.8-slim
   WORKDIR /app
   COPY . /app
   RUN pip install --no-cache-dir flask
   EXPOSE 5000
   CMD ["python", "app.py"]

---
# 4 Build Docker image
1. Build:
   sudo docker build -t flask-apparmor .

2. Verify image exists:
   sudo docker images | grep flask-apparmor

---
# 5 Create AppArmor profile (final secure profile)
1. Open file (as root):
   sudo nano /etc/apparmor.d/my-apparmor-profile

2. Paste the exact profile below and save:
   #include <tunables/global>
   profile my-apparmor-profile flags=(attach_disconnected) {
     # Deny sensitive directories first
     deny /etc/** rwmklx,
     deny /var/** rwmklx,
     # Deny common shells
     deny /bin/sh x,
     deny /usr/bin/sh x,
     deny /bin/dash x,
     deny /usr/bin/dash x,
     deny /bin/bash x,
     deny /usr/bin/bash x,
     # Allow Python interpreter(s)
     /usr/local/bin/python rix,
     /usr/local/bin/python3 rix,
     /usr/local/bin/python3.8 rix,
     # Allow Python libraries (read + mmap)
     /usr/local/lib/** mr,
     /usr/lib/** mr,
     /lib/** mr,
     /lib64/** mr,
     # Basic container files
     /etc/ld.so.cache r,
     /etc/hosts r,
     /etc/resolv.conf r,
     /proc/** r,
     /sys/** r,
     # Networking for Flask
     network inet stream,
     # Application directory
     /app/** rwk,
     # Capabilities
     capability net_bind_service,
     deny capability sys_admin,
   }

---
# 6 Load & enforce profile
1. Reload profile:
   sudo apparmor_parser -r /etc/apparmor.d/my-apparmor-profile

2. Enforce:
   sudo aa-enforce /etc/apparmor.d/my-apparmor-profile

3. Verify:
   sudo aa-status | grep my-apparmor-profile
   # Expected: my-apparmor-profile (enforce)

If you see "Skipping profile in /etc/apparmor.d/disable", move the file out of disable/:
   sudo mv /etc/apparmor.d/disable/my-apparmor-profile /etc/apparmor.d/
   then repeat reload & enforce.

---
# 7 Run Flask container under AppArmor
1. Start container:
   sudo docker run --security-opt apparmor=my-apparmor-profile -p 5000:5000 --name flask-secure-instance -d flask-apparmor

2. Confirm it's running:
   sudo docker ps

3. Access app in browser or curl:
   curl http://localhost:5000

---
# 8 Manual tests (verify restrictions)
1. Find container id or name (example uses name flask-secure-instance):
   sudo docker ps

2. Attempt to read sensitive file (should be denied):
   sudo docker exec -it flask-secure-instance cat /etc/passwd
   # Expected: "Permission denied" or empty output

3. Attempt to spawn a shell (should be denied or command not present):
   sudo docker exec -it flask-secure-instance /bin/sh
   # Expected: "permission denied" OR "not found" if shell absent

4. Try writing to /var (should be denied):
   sudo docker exec -it flask-secure-instance sh -c "echo hi > /var/test" 
   # Expected: "Permission denied" or failure

5. If Docker cannot stop the container (permission denied), kill it:
   sudo docker kill flask-secure-instance
   sudo docker rm flask-secure-instance

---
# 9 Python automation (detailed steps)
## 9.1 Install SDK (host)
1. If not installed:
   pip3 install --user docker
2. Make sure ~/.local/bin is in PATH, or run with full python3 -m pip / python path.

## 9.2 apply_apparmor.py — purpose & how to run
1. Create file apply_apparmor.py with this content:
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
   print("HostConfig.SecurityOpt:", info.get('HostConfig',{}).get('SecurityOpt'))
   # stop & remove for cleanup (optional)
   container.stop()
   container.remove()

2. Run (from project dir):
   python3 apply_apparmor.py
3. What to expect:
   - Build logs printed
   - "Container started: <short_id>"
   - HostConfig.SecurityOpt should include "apparmor=my-apparmor-profile"
4. Troubleshooting:
   - If inspect shows no SecurityOpt, the profile wasn't attached — ensure profile is enforced and name matches.

## 9.3 test_restricted_actions.py — purpose & how to run
1. Create file test_restricted_actions.py with this content:
   import docker, time
   client = docker.from_env()
   container = client.containers.run(
       "flask-apparmor",
       ports={'5000/tcp': 5000},
       security_opt=["apparmor=my-apparmor-profile"],
       detach=True,
       name="flask-secure-test"
   )
   time.sleep(1)  # let container initialize
   code, out = container.exec_run("cat /etc/passwd")
   print("Read /etc/passwd:", code, out.decode(errors='replace'))
   code, out = container.exec_run("/bin/sh -c 'echo shell-up'")
   print("Execute /bin/sh:", code, out.decode(errors='replace'))
   # Cleanup
   container.stop()
   container.remove()

2. Run:
   python3 test_restricted_actions.py

3. Expected outputs:
   - Read /etc/passwd: Exit Code 1 (or non-zero), Output indicates denied
   - Execute /bin/sh: Exit Code 126 or non-zero, Output indicates permission denied or empty

4. If outputs show success:
   - Confirm profile is enforced (sudo aa-status)
   - Confirm Docker attached the profile (docker inspect on container; HostConfig.SecurityOpt must list apparmor)
   - Adjust profile to deny required paths and reload with apparmor_parser

---
# 10 Cleanup & notes
1. To stop & remove containers:
   sudo docker ps
   sudo docker stop <container>
   sudo docker rm <container>

2. To unload profile:
   sudo aa-disable /etc/apparmor.d/my-apparmor-profile
   sudo apparmor_parser -R /etc/apparmor.d/my-apparmor-profile

3. Debug AppArmor denials:
   sudo journalctl -k | grep -i apparmor
   sudo dmesg | grep -i apparmor

4. Tune profile: start in complain mode while developing:
   sudo aa-complain /etc/apparmor.d/my-apparmor-profile
   # watch logs, then add required allow rules, then aa-enforce.

---
# 11 Final tips
- Always match the profile name passed to Docker with the profile name loaded in AppArmor.
- Use exact binary paths if you create executable-specific profiles; named profiles (profile my-apparmor-profile { ... }) are best for Docker.
- Use complain mode to learn required permissions, then move to enforce.
- Combine AppArmor with Docker features: --read-only, --cap-drop, seccomp, user namespaces for layered security.

---
END OF FILE
