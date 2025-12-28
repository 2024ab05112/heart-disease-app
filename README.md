# Heart Disease Prediction System - MLOps Assignment

This project demonstrates an end-to-end MLOps pipeline for a Heart Disease Prediction application. It consists of a FastAPI backend for model serving and a Django frontend for user interaction, deployed on Kubernetes (Minikube).

## Project Structure

- **backend/**:
    - **src/**: FastAPI application and ML logic.
    - **Dockerfile**: Backend build instructions.
    - **requirements.txt**: Python dependencies.
- **frontend/**: Django application (User Interface).
- **k8s/**: Kubernetes manifests.
    - **backend/**: Deployments for the API.
    - **frontend/**: Deployments for the UI.
    - **monitoring/**: Prometheus and Grafana manifests.
    - **common/**: Ingress references.
- **docs/**: Project documentation, reports, and assignment files.

## How to Run (Minikube)

### Prerequisites
- Docker
- Minikube
- Kubectl

### Step 1: Start Minikube
```bash
minikube start
```

### Step 2: Build and Push Docker Images
We need to build the images and push them to Docker Hub so Kubernetes can pull them.

**(First, log in to Docker Hub: `docker login`)**

**Backend Image:**
```bash
docker build -t 2024ab05112/heart-disease-api:latest backend/
docker push 2024ab05112/heart-disease-api:latest
```

**Frontend Image:**
```bash
docker build -t 2024ab05112/heart-disease-frontend:latest frontend/
docker push 2024ab05112/heart-disease-frontend:latest
```

### Step 3: Deploy to Kubernetes
Apply the Kubernetes manifests from the organized directories.

```bash
# Deploy Backend & Frontend
kubectl apply -f k8s/backend/
kubectl apply -f k8s/frontend/
kubectl apply -f k8s/common/

# Deploy Monitoring Stack (Optional)
kubectl apply -f k8s/monitoring/
```

### Step 4: Access the Application

**Frontend UI:**
To access the web interface:
```bash
minikube service heart-disease-frontend-service --url
```
Example Output: `http://192.168.49.2:30008`

**Monitoring (Grafana):**
```bash
minikube service grafana --url
```

## Architecture

1.  **Frontend (Django)**: 
    - Exposed via NodePort 30008.
    - Collects user input via a web form.
    - Sends POST requests to the backend service.
    
2.  **Backend (FastAPI)**:
    - Exposed via NodePort 30007 (and internally on port 80).
    - Loads the trained ML model (exported_model).
    - Processes requests and returns predictions.

3.  **Communication**: The Frontend talks to the Backend using the internal K8s DNS name status http://heart-disease-service:80.

For a detailed breakdown of the service connections and a visual workflow diagram, please refer to [SERVICE_ARCHITECTURE.md](SERVICE_ARCHITECTURE.md).