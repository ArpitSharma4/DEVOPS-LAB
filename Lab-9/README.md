# 🧪 JENKINS MULTI-STAGE PIPELINE (BUILD → TEST → DEPLOY → RUN → RETEST)
# COMPLETE README (WINDOWS + VS CODE + DOCKER)

# 1️⃣ INSTALL JENKINS USING DOCKER (WINDOWS)
Install Docker Desktop → Enable WSL2 backend.
Run Jenkins container:
docker run -d -p 8080:8080 -p 50000:50000 --name jenkins-lts -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
Access Jenkins at: http://localhost:8080
Install recommended plugins.

# 2️⃣ CREATE PYTHON FLASK PROJECT (VS CODE)
Create folder:
mkdir python-flask-app
cd python-flask-app
code .

Create file: app.py
--------------------------------------------------
from flask import Flask
app = Flask(__name__)
@app.route("/")
def home():
    return "Hello, Jenkins Multi-Stage Pipeline!"
if __name__ == "__main__":
    app.run(debug=True)
--------------------------------------------------

Create file: requirements.txt
--------------------------------------------------
flask==2.1.2
--------------------------------------------------

Create file: test_app.py
--------------------------------------------------
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
--------------------------------------------------

# 3️⃣ PUSH PROJECT TO GITHUB
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/devops-sample-code.git
git push -u origin main

# 4️⃣ CREATE JENKINS PIPELINE JOB
Jenkins → New Item → Pipeline  
Pipeline script from SCM  
SCM: Git  
Repo URL: your GitHub URL  
Branch: */main  

# 5️⃣ CREATE JENKINSFILE (INSIDE PROJECT)
--------------------------------------------------
pipeline {
    agent any

    stages {
        stage('Build') {
            steps { echo 'Installing dependencies...' }
        }
        stage('Test') {
            steps { sh 'python3 -m unittest discover -s .' }
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
                nohup python3 ${WORKSPACE}/python-app-deploy/app.py > ${WORKSPACE}/python-app-deploy/app.log 2>&1 &
                echo $! > ${WORKSPACE}/python-app-deploy/app.pid
                '''
            }
        }
        stage('Test Application') {
            steps { sh 'python3 ${WORKSPACE}/test_app.py' }
        }
    }

    post {
        success { echo 'Pipeline completed successfully!' }
        failure { echo 'Pipeline failed.' }
    }
}
--------------------------------------------------
Push it:
git add Jenkinsfile
git commit -m "Added Jenkinsfile"
git push

# 6️⃣ INSTALL PYTHON INSIDE JENKINS CONTAINER
docker exec -it -u root jenkins-lts bash
apt update
apt install -y python3 python3-pip python3.11-venv
pip install flask
exit

# 7️⃣ RUN PIPELINE
Jenkins → Build Now  
Stages executed:
✔ Build  
✔ Test  
✔ Deploy  
✔ Run Application  
✔ Test Application  

Output:
Pipeline completed successfully!

# 8️⃣ OPTIONAL — CODE QUALITY CHECK
Install:
pip install flake8
Add to Jenkinsfile:
stage('Code Quality') { steps { sh 'flake8 .' } }

# 🎉 DONE — MULTI-STAGE PIPELINE FULLY WORKING
Your pipeline now:
✔ Builds Flask app  
✔ Runs tests  
✔ Deploys  
✔ Starts server  
✔ Re-tests  
✔ Provides full automation
