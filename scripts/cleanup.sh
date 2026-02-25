#!/bin/bash

set -e

echo "Cleaning up Red Hat OpenShift AI Workload Solution"
echo "=================================================="

read -p "Are you sure you want to delete all resources? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cleanup cancelled."
    exit 0
fi

echo "Deleting namespace and all resources..."
oc delete namespace ai-workload --ignore-not-found=true

echo "Cleanup completed successfully!"
