#!/bin/bash

set -e

echo "Setting up Red Hat OpenShift AI Workload Solution"
echo "=================================================="

if ! command -v oc &> /dev/null; then
    echo "Error: OpenShift CLI (oc) not found. Please install it first."
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo "Error: Helm not found. Please install it first."
    exit 1
fi

echo "Checking OpenShift connection..."
oc whoami || { echo "Error: Not logged into OpenShift"; exit 1; }

echo "Creating namespace..."
oc apply -f k8s/namespace.yaml

echo "Applying resource quota..."
oc apply -f k8s/resourcequota.yaml

echo "Applying network policy..."
oc apply -f k8s/networkpolicy.yaml

echo "Creating ConfigMap..."
oc apply -f k8s/configmap.yaml

echo "Deploying application..."
oc apply -f k8s/deployment.yaml
oc apply -f k8s/service.yaml
oc apply -f k8s/route.yaml
oc apply -f k8s/hpa.yaml
oc apply -f k8s/pdb.yaml
oc apply -f k8s/servicemonitor.yaml

echo "Waiting for deployment to be ready..."
oc rollout status deployment/ai-inference -n ai-workload --timeout=5m

echo "Getting route URL..."
ROUTE_URL=$(oc get route ai-inference-route -n ai-workload -o jsonpath='{.spec.host}')

echo ""
echo "=================================================="
echo "Deployment completed successfully!"
echo "Application URL: https://$ROUTE_URL"
echo "=================================================="
echo ""
echo "Useful commands:"
echo "  View pods: oc get pods -n ai-workload"
echo "  View logs: oc logs -f deployment/ai-inference -n ai-workload"
echo "  View HPA: oc get hpa -n ai-workload"
echo "  Scale manually: oc scale deployment/ai-inference --replicas=5 -n ai-workload"
