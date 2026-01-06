# Heart Disease Prediction: End-to-End MLOps Solution

[![CI/CD Pipeline](https://github.com/2024ab05112/heart-disease-app/actions/workflows/deploy.yml/badge.svg)](https://github.com/2024ab05112/heart-disease-app/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready machine learning system for heart disease risk prediction, featuring automated CI/CD, experiment tracking with MLflow, and scalable deployment on Azure Kubernetes Service (AKS).

## Live Access
The entire stack is accessible via a single entry point using Ingress routing:
- **Web Application:** [Frontend UI](http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/)
- **API Documentation:** [Swagger UI](http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/api/docs)
- **Monitoring:** [Grafana Dashboard](http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/grafana/) | [Prometheus UI](http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/prometheus/)

---

## Professional Documentation
For comprehensive details on EDA, modelling choices, experiment tracking, and pipeline design, please refer to the official project reports:
- [**Project Report**](docs/Project_Report.docx) ([Markdown Version](docs/Project_Report.md))
- [**Technical Overview**](docs/Detailed_Project_Report.docx) ([Markdown Version](docs/Detailed_Project_Report.md))
- [**Project Detail Description**](https://drive.google.com/file/d/1EAkUQg3R94hodZxZxqRHMX2v1R3LgmU4/view)

---

## System Architecture
The system utilizes a unified microservices architecture routed via a high-performance Nginx Ingress Controller.

```mermaid
graph TD
    User((User)) -->|Single IP| Ingress[Nginx Ingress]
    Ingress -->|/| Frontend[Frontend Web]
    Ingress -->|/api| Backend[Backend API]
    Ingress -->|/grafana| Grafana[Grafana]
    Ingress -->|/prometheus| Prometheus[Prometheus]
    
    Frontend -->|ClusterIP Comms| Backend
    Backend -->|Metrics| Prometheus
    Prometheus -->|DB Query| Grafana
```

---

## Quick Start (Local Setup)

The easiest way to run the entire stack locally is via Docker Compose. This will build all images from scratch and orchestrate the services.

### 1. Prerequisites
- Docker & Docker Compose installed.
- Repository cloned.

### 2. Execution
```bash
# Build and start all services (Backend, Frontend, MLflow)
docker-compose up --build
```
The application will be available at http://localhost.

---

## CI/CD Workflow
The project follows a robust automation lifecycle via GitHub Actions:
1. **Linting & Testing:** Automated checks using flake8 and pytest.
2. **Containerization:** Concurrent Docker builds for high efficiency.
3. **Deployment:** Automated rollout to Azure Kubernetes Service on every push to main.

---
*Developed as part of the MLOps Assignment*