# Azure Kubernetes Service (AKS) Deployment Guide

This guide details how the Heart Disease Prediction System is deployed to a production-grade Kubernetes environment using Azure Kubernetes Service (AKS) and GitHub Actions.

## Infrastructure Overview

The application runs on an AKS cluster (`HeartDiseaseCluster`) within the `HeartDiseaseRG` resource group. 
To optimize costs for development/student usage, the cluster is designed to be **started on demand** by the CI/CD pipeline and should be **stopped manually** when not in use.

## CI/CD Pipeline (`deploy.yml`)

The project uses a sophisticated GitHub Actions workflow located at `.github/workflows/deploy.yml` that handles the entire deployment process.

### Triggers
The pipeline runs automatically on:
- **Push to `main` branch**: Only if changes are detected in `backend/`, `frontend/`, or `k8s/` directories (ignoring docs).
- **Manual Dispatch**: Can be triggered manually from the "Actions" tab in GitHub.

### Pipeline Stages

1.  **Check Changes (`check-changes`)**:
    - Analyzes which parts of the codebase (Backend, Frontend, or K8s manifests) have changed.
    - This creates a "Smart Build" process: we only rebuild docker images if the application code has changed.

2.  **Build and Push (`build-and-push`)**:
    - Runs only if backend or frontend code changes.
    - Builds Docker images.
    - Pushes images to Docker Hub with two tags:
        - `latest`: For general usage.
        - `<commit-sha>`: For precise version tracking and rolling updates.

3.  **Deploy (`deploy`)**:
    - **Azure Login**: Authenticates using the `AZURE_CREDENTIALS` secret.
    - **Cluster State Check**: Automatically checks if the AKS cluster is `Stopped`. If so, it sends a command to **Start** it.
    - **Context Setup**: Configures `kubectl` to talk to the AKS cluster using `kubelogin`.
    - **Dynamic Manifest Update**:
        - Replaces the image tags in the Kubernetes manifests (`deployment.yml` files) with the specific `<commit-sha>` generated in the build step.
        - This ensures that the cluster runs exactly the version of code that triggered the pipeline.
    - **Apply Manifests**: Applies all configurations from `k8s/backend`, `k8s/frontend`, `k8s/monitoring`, and `k8s/common`.

## Secrets Configuration

For the pipeline to work, the following secrets must be configured in the GitHub Repository (Settings -> Secrets and variables -> Actions):

| Secret Name | Description |
|-------------|-------------|
| `DOCKER_USERNAME` | Your Docker Hub username. |
| `DOCKER_PASSWORD` | Your Docker Hub access token (or password). |
| `AZURE_CREDENTIALS` | The JSON output from creating an Azure Service Principal. |

## Manual Cluster Management

While the pipeline *starts* the cluster, it does **not** stop it to prevent accidental downtime during review. You must stop it manually to save costs.

**Stop Cluster:**
```bash
az aks stop --resource-group HeartDiseaseRG --name HeartDiseaseCluster
```

**Start Cluster (Manual):**
```bash
az aks start --resource-group HeartDiseaseRG --name HeartDiseaseCluster
```

**Get Credentials for Local `kubectl`:**
```bash
az aks get-credentials --resource-group HeartDiseaseRG --name HeartDiseaseCluster
```
