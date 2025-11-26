# 🚀 PRACTICAL — JENKINS HELLO WORLD JOB
# =====================================

# =====================================
# ✅ 1. Create a GitHub Repository
# =====================================
1. Go to https://github.com  
2. Click **New Repository**  
3. Name → `devops-sample-code`  
4. Make it **Public**  
5. Click **Create Repository**  

---

# =====================================
# ✅ 2. Create a Personal Access Token (Classic)
# =====================================
1. Visit: https://github.com/settings/tokens  
2. Open **Tokens (classic)**  
3. Click **Generate new token (classic)**  
4. Name: `jenkins-token`  
5. Expiry: 90 days  
6. Scope: **repo**  
7. Click Generate  
8. Copy the token  

---

# =====================================
# ✅ 3. Create Script Locally (Windows)
# =====================================
mkdir devops-sample-code  
cd devops-sample-code  
New-Item hello-world.sh  
notepad hello-world.sh  

Paste:
#!/bin/bash  
echo "Hello, Jenkins!"

---

# =====================================
# ✅ 4. Initialize Git
# =====================================
git init  
git config --global user.name "Your Name"  
git config --global user.email "your-email@example.com"  

---

# =====================================
# ✅ 5. Add & Commit Script
# =====================================
git add hello-world.sh  
git commit -m "Added hello-world script"  

---

# =====================================
# ✅ 6. Connect Local Repo to GitHub
# =====================================
git remote add origin https://github.com/<username>/devops-sample-code.git  

---

# =====================================
# ✅ 7. Push to GitHub
# =====================================
git push -u origin main  

Login:  
Username → GitHub username  
Password → PAT token  

🎉 Script is now in GitHub.

---

# =====================================
# ⚙️ 8. Install & Run Jenkins (Docker)
# =====================================

docker run -d -p 8080:8080 -p 50000:50000 --name jenkins jenkins/jenkins:lts  

Check:
docker ps  

---

# =====================================
# 🔑 9. Get Jenkins Admin Password
# =====================================

docker exec -it jenkins bash  
cat /var/jenkins_home/secrets/initialAdminPassword  

Open Jenkins:  
http://localhost:8080  
Paste password → continue setup  

---

# =====================================
# 🔐 10. Add GitHub Credentials in Jenkins
# =====================================
Jenkins → Manage Jenkins → Credentials → System → Global → Add Credentials  

- Username → GitHub username  
- Password → PAT token  
- ID → `github-creds`  

Save.

---

# =====================================
# 🏗 11. Create Freestyle Job
# =====================================
1. Dashboard → New Item  
2. Name: `HelloWorld`  
3. Select → Freestyle Project  
4. Click OK  

---

# =====================================
# ⚙️ 12. Configure Job
# =====================================

## 🔹 Source Code Management → Git
Repository URL:  
https://github.com/<username>/devops-sample-code.git  

Credentials → github-creds  

## 🔹 Build Step → Execute Shell
sh hello-world.sh  

---

# =====================================
# 🚀 13. Run the Job
# =====================================
Click **Build Now**  

---

# =====================================
# 🎉 14. Expected Output
# =====================================
Hello, Jenkins!  
Finished: SUCCESS  

---

# 🎯 Final Result
You now have a fully working Jenkins CI pipeline integrated with GitHub on Windows.
