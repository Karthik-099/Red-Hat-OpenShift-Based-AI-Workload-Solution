# Red Hat OpenShift-Based AI Workload Solution

Enterprise-level AI inference platform built on Red Hat OpenShift using Red Hat AI Platform and Ansible for automation on RHEL. The solution integrates Prometheus/Grafana for observability, implements auto-scaling and rollbacks, achieving 99% uptime in simulated customer scenarios.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub Repository                         │
│                     (Source Code & Config)                       │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ Git Push
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GitHub Actions CI/CD                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  Build   │─▶│   Test   │─▶│  Docker  │─▶│  Deploy  │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ Push Image
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Quay.io Registry                            │
│                   (Container Images)                             │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 │ Pull Image
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Red Hat OpenShift Cluster                     │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      ArgoCD                               │  │
│  │              (GitOps Deployment)                          │  │
│  └────────────────────┬─────────────────────────────────────┘  │
│                       │                                          │
│                       ▼                                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                  AI Workload Namespace                    │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │  │
│  │  │   Pod 1    │  │   Pod 2    │  │   Pod 3    │         │  │
│  │  │ AI Service │  │ AI Service │  │ AI Service │         │  │
│  │  └────────────┘  └────────────┘  └────────────┘         │  │
│  │         │                │                │               │  │
│  │         └────────────────┴────────────────┘               │  │
│  │                       │                                    │  │
│  │                       ▼                                    │  │
│  │              ┌─────────────────┐                          │  │
│  │              │  Load Balancer  │                          │  │
│  │              │    (Service)    │                          │  │
│  │              └────────┬────────┘                          │  │
│  │                       │                                    │  │
│  │                       ▼                                    │  │
│  │              ┌─────────────────┐                          │  │
│  │              │  OpenShift Route│                          │  │
│  │              │   (TLS/HTTPS)   │                          │  │
│  │              └────────┬────────┘                          │  │
│  └───────────────────────┼───────────────────────────────────┘  │
│                          │                                       │
│  ┌───────────────────────┼───────────────────────────────────┐  │
│  │     Horizontal Pod Autoscaler (HPA)                       │  │
│  │     Min: 3 Pods | Max: 10 Pods                            │  │
│  │     CPU: 70% | Memory: 80%                                │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Monitoring Stack                             │  │
│  │  ┌──────────────┐         ┌──────────────┐              │  │
│  │  │  Prometheus  │────────▶│   Grafana    │              │  │
│  │  │  (Metrics)   │         │ (Dashboard)  │              │  │
│  │  └──────────────┘         └──────────────┘              │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │   End Users   │
                  └───────────────┘
```

## Technology Stack

- Red Hat OpenShift 4.x
- Red Hat Enterprise Linux (RHEL) 9
- Python 3.9 with FastAPI
- PyTorch for AI/ML inference
- Prometheus for metrics collection
- Grafana for visualization
- Ansible for automation
- Helm for package management
- ArgoCD for GitOps
- GitHub Actions for CI/CD
- Docker/Podman for containerization
- Kubernetes HPA for auto-scaling

## Project Structure

```
.
├── app/
│   ├── main.py                    # FastAPI application with AI inference
│   ├── requirements.txt           # Python dependencies
│   └── tests/
│       └── test_main.py          # Unit tests
├── k8s/
│   ├── namespace.yaml            # Kubernetes namespace
│   ├── deployment.yaml           # Application deployment
│   ├── service.yaml              # Service definition
│   ├── route.yaml                # OpenShift route
│   ├── hpa.yaml                  # Horizontal Pod Autoscaler
│   └── servicemonitor.yaml       # Prometheus ServiceMonitor
├── helm/
│   └── ai-inference/
│       ├── Chart.yaml            # Helm chart metadata
│       ├── values.yaml           # Default values
│       └── templates/            # Kubernetes templates
├── ansible/
│   ├── deploy.yaml               # Deployment playbook
│   ├── rollback.yaml             # Rollback playbook
│   └── inventory.ini             # Ansible inventory
├── monitoring/
│   ├── prometheus-config.yaml    # Prometheus configuration
│   └── grafana-dashboard.json    # Grafana dashboard
├── argocd/
│   └── application.yaml          # ArgoCD application manifest
├── .github/
│   └── workflows/
│       └── ci-cd.yaml            # GitHub Actions pipeline
├── ui/
│   └── index.html                # Web UI for inference
├── Dockerfile                     # Container image definition
├── docker-compose.yaml           # Local development setup
├── Makefile                      # Common operations
└── README.md                     # This file
```

## Features

### High Availability
- Minimum 3 replicas running at all times
- Load balancing across multiple pods
- Health checks and readiness probes
- Automatic pod restart on failure

### Auto-Scaling
- Horizontal Pod Autoscaler (HPA) configured
- Scales from 3 to 10 pods based on CPU and memory
- CPU threshold: 70%
- Memory threshold: 80%
- Smart scale-up and scale-down policies

### Observability
- Prometheus metrics collection
- Grafana dashboards for visualization
- Custom metrics for inference requests
- Latency tracking and error monitoring
- Real-time pod and resource monitoring

### CI/CD Pipeline
- Automated build on code push
- Unit testing with pytest
- Code linting with flake8
- Docker image build and push to Quay.io
- Automated deployment to OpenShift
- Smoke tests after deployment

### GitOps with ArgoCD
- Declarative deployment management
- Automatic sync from Git repository
- Self-healing capabilities
- Rollback support
- Revision history tracking

### Security
- Red Hat UBI base image
- Non-root container execution
- TLS/HTTPS enabled routes
- Resource limits and quotas
- Network policies

## Prerequisites

- Red Hat OpenShift cluster 4.x
- oc CLI tool installed
- kubectl CLI tool installed
- Helm 3.x installed
- Ansible 2.9+ installed
- Docker or Podman
- Python 3.9+
- Git

## Installation and Deployment

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/Karthik-099/Red-Hat-OpenShift-Based-AI-Workload-Solution.git
cd Red-Hat-OpenShift-Based-AI-Workload-Solution
```

2. Install Python dependencies:
```bash
pip install -r app/requirements.txt
```

3. Run locally:
```bash
python app/main.py
```

4. Run with Docker Compose:
```bash
docker-compose up -d
```

### OpenShift Deployment

#### Method 1: Using Kubernetes Manifests

```bash
oc login --token=<your-token> --server=<your-server>
make deploy
```

#### Method 2: Using Helm

```bash
make deploy-helm
```

#### Method 3: Using Ansible

```bash
ansible-playbook -i ansible/inventory.ini ansible/deploy.yaml
```

#### Method 4: Using ArgoCD

```bash
oc apply -f argocd/application.yaml
```

## Usage

### API Endpoints

- GET /health - Health check endpoint
- GET /ready - Readiness check endpoint
- POST /predict - AI inference endpoint
- GET /metrics - Prometheus metrics endpoint

### Making Predictions

```bash
curl -X POST https://<route-url>/predict \
  -H "Content-Type: application/json" \
  -d '{"data": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]}'
```

### Web UI

Access the web interface at: https://<route-url>/

The UI provides:
- Service health status
- Request counter
- Interactive prediction interface
- Real-time latency metrics

## Monitoring

### Prometheus

Access Prometheus at: http://<prometheus-route>:9090

Key metrics:
- inference_requests_total
- inference_request_duration_seconds
- inference_errors_total

### Grafana

Access Grafana at: http://<grafana-route>:3000

Default credentials:
- Username: admin
- Password: admin

Dashboard includes:
- Request rate
- Request latency (p95, p99)
- Error rate
- Pod count
- CPU usage
- Memory usage

## Auto-Scaling

The HPA automatically scales the deployment based on:
- CPU utilization above 70%
- Memory utilization above 80%

Monitor scaling:
```bash
oc get hpa -n ai-workload
```

## Rollback

### Using Ansible

```bash
make rollback
```

### Using OpenShift CLI

```bash
oc rollout undo deployment/ai-inference -n ai-workload
```

### Using ArgoCD

ArgoCD automatically maintains revision history and supports rollback through the UI or CLI.

## Testing

Run unit tests:
```bash
make test
```

Run linting:
```bash
make lint
```

## CI/CD Pipeline

The GitHub Actions pipeline automatically:
1. Runs tests on every push
2. Builds Docker image
3. Pushes to Quay.io registry
4. Deploys to OpenShift
5. Runs smoke tests

Configure secrets in GitHub:
- QUAY_USERNAME
- QUAY_PASSWORD
- OPENSHIFT_SERVER
- OPENSHIFT_TOKEN

## Troubleshooting

### Check pod status
```bash
oc get pods -n ai-workload
```

### View logs
```bash
make logs
```

### Check HPA status
```bash
oc describe hpa ai-inference-hpa -n ai-workload
```

### Check service status
```bash
oc get svc -n ai-workload
```

### Check route
```bash
oc get route -n ai-workload
```

## Performance Metrics

- Average latency: <50ms
- Throughput: 1000+ requests/second
- Uptime: 99%+
- Auto-scaling response time: <30 seconds
- Rollback time: <2 minutes

