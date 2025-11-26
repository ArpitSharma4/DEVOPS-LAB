# 🧪 Lab 4 – Jenkins Multi-Stage CI Pipeline (Build → Test → Deploy → Run → Retest)
# 📘 Complete Step-By-Step Guide (Windows + VS Code + Docker)

---

## 1️⃣ INSTALL JENKINS USING DOCKER (WINDOWS)

Install Docker Desktop → enable WSL2 backend.

Run Jenkins:
docker run -d -p 8080:8080 -p 50000:50000 --name jenkins-lts -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts

Access Jenkins:
http://localhost:8080

Install “Recommended Plugins”.

---

## 2️⃣ CREATE PYTHON FLASK PROJECT (VS CODE)

Create folder:
mkdir python-flask-app
cd python-flask-app
code .

### FILE: app.py
from flask import Flask
app = Flask(__name__)
@app.route("/")
def home():
    return "Hello, Jenkins Multi-Stage Pipeline!"
if __name__ == "__main__":
    app.run(debug=True)

### FILE: requirements.txt
flask==2.1.2

### FILE: test_app.py
import unittest
from app import app
class TestApp(unittest.TestCase):
    def test_home(self):
        tester = app.test_client()
        response = tester.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "Hello, Jenkins Multi-Stage Pipeline!")
if __name__ == "__main__":
    unittest.main()

---

## 3️⃣ PUSH PROJECT TO GITHUB

git init  
git add .  
git commit -m "Initial commit"  
git branch -M main  
git remote add origin https://github.com/<username>/devops-sample-code.git  
git push -u origin main  

---

## 4️⃣ CREATE JENKINS PIPELINE JOB

Jenkins → New Item → *Pipeline*   
Pipeline script from SCM  
SCM: Git  
Repo URL: your GitHub repo  
Branch: */main  

---

## 5️⃣ CREATE JENKINSFILE (FULL MULTI-STAGE PIPELINE)

pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                echo 'Installing dependencies...'
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m unittest discover -s .'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                mkdir -p ${WORKSPACE}/python-app-deploy
                cp ${WORKSPACE}/app.py ${WORKSPACE}/python-app-deploy/
                '''
            }
        }

        stage('Run Application') {
            steps {
                sh '''
                nohup python3 ${WORKSPACE}/python-app-deploy/app.py \
                > ${WORKSPACE}/python-app-deploy/app.log 2>&1 &
                echo $! > ${WORKSPACE}/python-app-deploy/app.pid
                '''
            }
        }

        stage('Test Application') {
            steps {
                sh 'python3 ${WORKSPACE}/test_app.py'
            }
        }
    }

    post {
        success { echo 'Pipeline completed successfully!' }
        failure { echo 'Pipeline failed.' }
    }
}

Push it:
git add Jenkinsfile  
git commit -m "Added Jenkinsfile"  
git push  

---

## 6️⃣ INSTALL PYTHON INSIDE JENKINS CONTAINER

docker exec -it -u root jenkins-lts bash  
apt update  
apt install -y python3 python3-pip python3.11-venv  
pip install flask  
exit  

---

## 7️⃣ RUN PIPELINE

Build Now → Output:

✔ Build  
✔ Test  
✔ Deploy  
✔ Run Application  
✔ Test Application  

Pipeline completed successfully!

---

## 8️⃣ OPTIONAL — ADD CODE QUALITY

pip install flake8  

Add stage to Jenkinsfile:
stage('Code Quality') { steps { sh 'flake8 .' } }

---

## 🎉 FINAL OUTCOME

✔ Fully automated CI pipeline  
✔ Flask app tested, deployed, and re-tested  
✔ Works on Windows + VS Code + Docker + Jenkins  

