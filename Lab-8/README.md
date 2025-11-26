# 🚀 PRACTICAL — JENKINS HELLO WORLD JOB

---

# 1️⃣ Create a GitHub Repository
1. Go to https://github.com  
2. Click **New Repository**  
3. Name → `devops-sample-code`  
4. Set to **Public**  
5. Click **Create Repository**

---

# 2️⃣ Create a Personal Access Token (Classic)
1. Visit: https://github.com/settings/tokens  
2. Open **Tokens (classic)**  
3. Click **Generate new token (classic)**  
4. Name: `jenkins-token`  
5. Expiry: **90 days**  
6. Enable scope: **repo**  
7. Click Generate  
8. Copy the token

---

# 3️⃣ Create Script Locally (Windows)

```bash
mkdir devops-sample-code
cd devops-sample-code
New-Item hello-world.sh
notepad hello-world.sh
```

Paste inside the file:
```bash
#!/bin/bash
echo "Hello, Jenkins!"
```

---

# 4️⃣ Initialize Git

```bash
git init
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

---

# 5️⃣ Add & Commit Script

```bash
git add hello-world.sh
git commit -m "Added hello-world script"
```

---

# 6️⃣ Connect Local Repo to GitHub

```bash
git remote add origin https://github.com/<username>/devops-sample-code.git
```

---

# 7️⃣ Push to GitHub

```bash
git push -u origin main
```

Login Prompt:  
- **Username:** your GitHub username  
- **Password:** your PAT token  

Script is now in GitHub ✔

---

# 8️⃣ Install & Run Jenkins (Docker)

```bash
docker run -d -p 8080:8080 -p 50000:50000 --name jenkins jenkins/jenkins:lts
```

Check container:
```bash
docker ps
```

---

# 9️⃣ Get Jenkins Admin Password

```bash
docker exec -it jenkins bash
cat /var/jenkins_home/secrets/initialAdminPassword
```

Open Jenkins:  
http://localhost:8080  
Paste password → Continue Setup

---

# 🔟 Add GitHub Credentials in Jenkins
Jenkins → Manage Jenkins → Credentials → System → Global → Add Credentials  

- Username → GitHub username  
- Password → PAT token  
- ID → `github-creds`  

Save.

---

# 1️⃣1️⃣ Create Freestyle Job
Dashboard → **New Item**  
Name → `HelloWorld`  
Select → **Freestyle Project**  
Click **OK**

---

# 1️⃣2️⃣ Configure Job

## Source Code Management → Git
Repository URL:
```
https://github.com/<username>/devops-sample-code.git
```
Credentials → `github-creds`

## Build Step → Execute Shell
```bash
sh hello-world.sh
```

---

# 1️⃣3️⃣ Run the Job
Click **Build Now**

---

# 1️⃣4️⃣ Expected Output
```
Hello, Jenkins!
Finished: SUCCESS
```

---

# 🎯 Final Result
You now have a **working Jenkins CI pipeline** integrated with GitHub on Windows.

---
