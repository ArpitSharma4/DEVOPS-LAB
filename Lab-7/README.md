# ================================
# STEP 1 — REMOVE OLD JENKINS
# ================================
docker rm -f jenkins

# ================================
# STEP 2 — RUN JENKINS (WITH DOCKER ACCESS)
# Required for CI pipelines to run Docker builds
# ================================
docker run -d --name jenkins `
 -p 8080:8080 -p 50000:50000 `
 -v jenkins_home:/var/jenkins_home `
 -v //var/run/docker.sock:/var/run/docker.sock `
 jenkins/jenkins:lts

# ================================
# STEP 3 — VERIFY JENKINS IS RUNNING
# ================================
docker ps

# ================================
# STEP 4 — GET INITIAL ADMIN PASSWORD
# ================================
docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# Copy the password → open Jenkins in browser:
# http://localhost:8080
# Enter password → Install Suggested Plugins → Create admin user → Continue

# ================================
# STEP 5 — CREATE NEW PIPELINE JOB
# (In Jenkins UI)
# ================================
# Jenkins Dashboard → New Item → Pipeline → OK
# Scroll to "Pipeline Script" → Paste below:

pipeline {
    agent any

    stages {

        stage('Pre-check Docker') {
            steps {
                sh 'docker --version'
                sh 'docker info'
            }
        }

        stage('Copy Files') {
            steps {
                script {
                    def src = "C:/DEV-1/Lab-6"
                    sh """
                        cp '${src}/delivery_metrics.py' .
                        cp '${src}/prometheus.yml' .
                        cp '${src}/alert_rules.yml' .
                    """
                }
            }
        }

        stage('Build Exporter Image') {
            steps {
                sh 'docker build -t delivery_metrics .'
            }
        }

        stage('Run Exporter') {
            steps {
                sh 'docker rm -f delivery_metrics || true'
                sh 'docker run -d -p 8000:8000 --name delivery_metrics delivery_metrics'
            }
        }

        stage('Run Prometheus') {
            steps {
                sh '''
                docker rm -f prometheus || true
                docker run -d --name prometheus -p 9090:9090 \
                 -v $WORKSPACE/prometheus.yml:/etc/prometheus/prometheus.yml \
                 -v $WORKSPACE/alert_rules.yml:/etc/prometheus/alert_rules.yml \
                 prom/prometheus
                '''
            }
        }

        stage('Run Grafana') {
            steps {
                sh '''
                docker rm -f grafana || true
                docker run -d --name grafana -p 4000:3000 grafana/grafana
                '''
            }
        }
    }
}

# ================================
# STEP 6 — RUN PIPELINE
# ================================
# In Jenkins:
# delivery-monitoring-pipeline → Build Now

# ================================
# STEP 7 — CHECK SERVICES
# ================================
# Python Exporter:
# http://localhost:8000/metrics

# Prometheus:
# http://localhost:9090

# Prometheus Targets:
# http://localhost:9090/targets

# Prometheus Alerts:
# http://localhost:9090/alerts

# Grafana:
# http://localhost:4000  (admin/admin)

# ================================
# STEP 8 — TRIGGER ALERTS
# ================================
# Edit delivery_metrics.py:
# Change:
pending = random.randint(10, 20)

# To:
pending = random.randint(50, 100)

# Restart exporter:
python delivery_metrics.py
