# DevOps Lab – Real-Time Monitoring & Alerting (Prometheus + Grafana + Jenkins)

# 1. Folder Structure
delivery_monitoring/
├── delivery_metrics.py
├── prometheus.yml
├── alert_rules.yml
└── Jenkinsfile

# 2. Python Exporter Setup
pip install prometheus-client

# delivery_metrics.py
from prometheus_client import start_http_server, Summary, Gauge
import random, time

total_deliveries = Gauge("total_deliveries", "Total number of deliveries")
pending_deliveries = Gauge("pending_deliveries", "Pending deliveries")
on_the_way_deliveries = Gauge("on_the_way_deliveries", "Deliveries on the way")
average_delivery_time = Summary("average_delivery_time_seconds", "Avg delivery time")

def simulate_delivery():
    pending = random.randint(10, 20)
    on_way = random.randint(5, 20)
    delivered = random.randint(30, 70)
    avg = random.uniform(15, 45)
    total = pending + on_way + delivered

    print(f"[INFO] Pending:{pending} OnWay:{on_way} Avg:{avg:.2f}s Total:{total}")

    pending_deliveries.set(pending)
    on_the_way_deliveries.set(on_way)
    total_deliveries.set(total)
    average_delivery_time.observe(avg)

if __name__ == "__main__":
    print("[INFO] Exporter running at :8000/metrics")
    start_http_server(8000)
    while True:
        simulate_delivery()
        time.sleep(1)

# Run exporter
python delivery_metrics.py

# 3. Prometheus Setup (prometheus.yml)
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: delivery_service
    static_configs:
      - targets: ["host.docker.internal:8000"]

rule_files:
  - "/etc/prometheus/alert_rules.yml"

# 4. Prometheus Alerts (alert_rules.yml)
groups:
  - name: delivery_alerts
    rules:
      - alert: HighPendingDeliveries
        expr: pending_deliveries > 10
        for: 15s
        labels: { severity: warning }
        annotations:
          summary: "High pending deliveries"
          description: "Pending > 10 for 15s."

      - alert: HighAverageDeliveryTime
        expr: (average_delivery_time_seconds_sum / average_delivery_time_seconds_count) > 30
        for: 15s
        labels: { severity: critical }
        annotations:
          summary: "High avg delivery time"
          description: "Avg > 30s for 15s."

# 5. Run Prometheus (PowerShell friendly)
docker rm -f prometheus
docker run -d --name prometheus -p 9090:9090 `
 -v C:\DEV-1\Lab-6\prometheus.yml:/etc/prometheus/prometheus.yml `
 -v C:\DEV-1\Lab-6\alert_rules.yml:/etc/prometheus/alert_rules.yml `
 prom/prometheus

# Prometheus URLs
http://localhost:9090
http://localhost:9090/targets
http://localhost:9090/alerts

# 6. Run Grafana
docker rm -f grafana
docker run -d --name grafana -p 4000:3000 grafana/grafana

# Grafana URL
http://localhost:4000  (admin/admin)

# 7. Grafana Panels (Run these as Queries)
total_deliveries
pending_deliveries
on_the_way_deliveries
average_delivery_time_seconds_sum / average_delivery_time_seconds_count

# 8. Trigger Alerts
# Modify in delivery_metrics.py:
pending = random.randint(50, 100)

# Restart:
python delivery_metrics.py

# Alerts will fire in:
http://localhost:9090/alerts

# 9. Jenkins Setup
docker rm -f jenkins
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 `
 -v jenkins_home:/var/jenkins_home `
 -v //var/run/docker.sock:/var/run/docker.sock `
 jenkins/jenkins:lts

# Get Jenkins password:
docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword

# Jenkins → New Item → Pipeline → paste Jenkinsfile below

# 10. Jenkinsfile (VSCode compatible)
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

# 11. Final Validation Checklist
# 1. http://localhost:8000/metrics → Python exporter OK
# 2. http://localhost:9090/targets → Prometheus target UP
# 3. http://localhost:9090/alerts → Alerts firing
# 4. http://localhost:4000 → Grafana dashboard working
# 5. Jenkins pipeline builds everything end-to-end

# End of README
