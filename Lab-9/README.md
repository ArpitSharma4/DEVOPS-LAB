# 🚀 Jenkins Multi-Stage Pipeline Exercise: Deploying a Python Application

This exercise demonstrates how to build a **complete CI/CD pipeline** in Jenkins using multiple stages:  
**Build → Test → Deploy → Run → Retest** for a Python Flask application.

---

# 🎯 Objective
Automate CI/CD for a Python Flask application using a Jenkins multi-stage pipeline.

Stages included:

- **Build** → Install dependencies  
- **Test** → Run unit tests  
- **Deploy** → Copy to deployment directory  
- **Run** → Launch the application  
- **Retest** → Test running app again  

---

# 🧰 Step 1: Set Up Jenkins
Install Jenkins on your system and ensure it is running.

Install required plugin:
- **Pipeline Plugin** (usually preinstalled)

---

# 🐍 Step 2: Create Python Flask Application

Create a project directory:

```bash
mkdir python-flask-app
cd python-flask-app
```

## `app.py`
```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Jenkins Multi-Stage Pipeline!"

if __name__ == "__main__":
    app.run(debug=True)
```

## `requirements.txt`
```
flask==2.1.2
```

## `test_app.py`
```python
import unittest
from app import app

class TestApp(unittest.TestCase):
    def test_home(self):
        tester = app.test_client()
        response = tester.get("/")
        print(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "Hello, Jenkins Multi-Stage Pipeline!")

if __name__ == "__main__":
    unittest.main()
```

---

# 🧑‍💻 Step 3: Push Code to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/<your-username>/devops-sample-code.git
git push -u origin main
```

---

# 🏗️ Step 4: Create Jenkins Multistage Pipeline Job
1. Open **Jenkins Dashboard**  
2. Click **New Item**  
3. Enter job name: `Python-MultiStage-Pipeline`  
4. Select **Pipeline**  
5. Click **OK**

---

# 📄 Step 5: Create Jenkinsfile

Create a file named **Jenkinsfile** in your repo:

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Creating virtual environment and installing dependencies...'
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'python3 -m unittest discover -s .'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying application...'
                sh '''
                mkdir -p ${WORKSPACE}/python-app-deploy
                cp ${WORKSPACE}/app.py ${WORKSPACE}/python-app-deploy/
                '''
            }
        }
        stage('Run Application') {
            steps {
                echo 'Running application...'
                sh '''
                nohup python3 ${WORKSPACE}/python-app-deploy/app.py > ${WORKSPACE}/python-app-deploy/app.log 2>&1 &
                echo $! > ${WORKSPACE}/python-app-deploy/app.pid
                '''
            }
        }
        stage('Test Application') {
            steps {
                echo 'Testing application...'
                sh 'python3 ${WORKSPACE}/test_app.py'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs for more details.'
        }
    }
}
```

Push Jenkinsfile:

```bash
git add Jenkinsfile
git commit -m "Added Jenkinsfile"
git push
```

---

# ⚙️ Step 6: Configure Jenkins Job

Inside Jenkins:

1. Job → **Configure**  
2. Pipeline section → Select **Pipeline script from SCM**  
3. SCM → Git  
4. Enter your repo URL  
5. Add credentials if required  
6. Save  

---

# ▶️ Step 7: Run the Pipeline

Click **Build Now** in Jenkins.

You will see the multi-stage execution:

- Build  
- Test  
- Deploy  
- Run Application  
- Test Application  

---

# 🛠️ Step 8: Fixing Jenkins Errors (Python Missing)

Inside Jenkins container:

Check running containers:
```bash
docker ps -a
```

Enter Jenkins container as root:
```bash
docker exec -it -u root <container-id> bash
```

Install required packages:

```bash
apt-get update
apt install python3
apt install pip
apt install python3.11-venv
apt install python3-flask
python3 -m unittest discover -s .
```

---

# ✅ Expected Outcome

### ✔ Build Stage  
Dependencies installed (Flask)

### ✔ Test Stage  
Unit tests run successfully

### ✔ Deploy Stage  
Application copied to:
```
/tmp/python-app-deploy
```

### ✔ Application Run  
Python Flask app starts in background

### ✔ Retest Stage  
Application tested again after deployment

### ✔ Final
Pipeline ends with:
```
Pipeline completed successfully!
Finished: SUCCESS
```

---

# 🚀 Additional Enhancements

## ✔ Add Code Quality Stage (flake8)
```groovy
stage('Code Quality') {
    steps {
        echo 'Running code quality checks...'
        sh 'flake8 .'
    }
}
```

## ✔ Deploy in Docker container  
Future improvement: containerize the Flask app.

## ✔ Add Notification Stage  
Email / Slack alerts on pipeline status.

---

# 🎉 End of README
