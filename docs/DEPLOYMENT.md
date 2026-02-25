# Deployment Guide

## Prerequisites

- Red Hat OpenShift 4.x cluster
- oc CLI authenticated to cluster
- Helm 3.x installed
- kubectl installed
- Quay.io account for container registry

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Karthik-099/Red-Hat-OpenShift-Based-AI-Workload-Solution.git
cd Red-Hat-OpenShift-Based-AI-Workload-Solution
```

### 2. Build Container Image

```bash
make build
make push
```

### 3. Deploy to OpenShift

```bash
./scripts/setup.sh
```

Or using Helm:

```bash
make deploy-helm
```

## Detailed Deployment Steps

### Step 1: Prepare OpenShift Cluster

Login to OpenShift:
```bash
oc login --token=<token> --server=<server-url>
```

### Step 2: Create Namespace

```bash
oc apply -f k8s/namespace.yaml
```

### Step 3: Apply Resource Quotas

```bash
oc apply -f k8s/resourcequota.yaml
```

### Step 4: Deploy Application

```bash
oc apply -f k8s/
```

### Step 5: Verify Deployment

```bash
oc get pods -n ai-workload
oc get svc -n ai-workload
oc get route -n ai-workload
```

### Step 6: Access Application

Get the route URL:
```bash
oc get route ai-inference-route -n ai-workload -o jsonpath='{.spec.host}'
```

## Configuration

### Environment Variables

Edit k8s/configmap.yaml:
- LOG_LEVEL: Logging level
- WORKERS: Number of worker processes
- MODEL_VERSION: Model version identifier

### Resource Limits

Edit k8s/deployment.yaml:
- CPU requests/limits
- Memory requests/limits

### Auto-scaling

Edit k8s/hpa.yaml:
- minReplicas: Minimum pod count
- maxReplicas: Maximum pod count
- CPU threshold
- Memory threshold

## Monitoring Setup

### Prometheus

ServiceMonitor is automatically created. Verify:
```bash
oc get servicemonitor -n ai-workload
```

### Grafana

Import dashboard from monitoring/grafana-dashboard.json

## Troubleshooting

### Pods not starting

```bash
oc describe pod <pod-name> -n ai-workload
oc logs <pod-name> -n ai-workload
```

### Service not accessible

```bash
oc get svc -n ai-workload
oc describe route ai-inference-route -n ai-workload
```

### HPA not scaling

```bash
oc describe hpa ai-inference-hpa -n ai-workload
oc get hpa -n ai-workload --watch
```

## Rollback

If deployment fails:
```bash
make rollback
```

Or manually:
```bash
oc rollout undo deployment/ai-inference -n ai-workload
```

## Cleanup

Remove all resources:
```bash
./scripts/cleanup.sh
```

Or manually:
```bash
oc delete namespace ai-workload
```
