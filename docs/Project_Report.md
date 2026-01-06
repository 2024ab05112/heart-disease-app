# Heart Disease Prediction: MLOps End-to-End Implementation Report

## 1. Project Overview
This project implements a scalable, reproducible, and production-ready Machine Learning solution for predicting the risk of heart disease based on patient health data. It utilizes the Heart Disease UCI Dataset and follows modern MLOps best practices.

### 1.1 Project Deliverables
- **GitHub Repository:** [https://github.com/2024ab05112/heart-disease-app.git](https://github.com/2024ab05112/heart-disease-app.git)
- **Unified Entry Point:** [http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/](http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/)
- **Application UI:** [Web Interface](http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/)
- **API Documentation:** [Swagger UI](http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/api/docs)
- **Monitoring (Grafana):** [Grafana Dashboard](http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/grafana/)
- **Metrics (Prometheus):** [Prometheus UI](http://heart-disease-2024ab05112.centralindia.cloudapp.azure.com/prometheus/)

---

## 2. System Architecture
The system is deployed on **Azure Kubernetes Service (AKS)** using an Ingress-based microservices architecture, optimized for high availability and observability.

### 2.1 Architecture Diagram
```mermaid
graph TD
    User((User)) -->|HTTP| Ingress[Nginx Ingress Controller]
    Ingress -->|/| Frontend[Frontend Pods]
    Ingress -->|/api| Backend[Backend API Pods]
    Ingress -->|/grafana| Grafana[Grafana]
    Ingress -->|/prometheus| Prometheus[Prometheus]
    
    Frontend -->|Internal RPC| Backend
    Backend -->|Log| MLflow[(MLflow)]
    Backend -->|Metrics| Prometheus
    Prometheus -->|Visualize| Grafana
```

---

## 3. Data Science & Experimentation

### 3.1 Exploratory Data Analysis (EDA)
- **Visualizations:** Generated histograms for feature distributions and a correlation heatmap to identify key predictors.
- **Insights:** Identified strong correlations between the target and features such as chest pain type (`cp`) and maximum heart rate (`thalach`).
- **Data Quality:** Verified zero missing values and handled categorical encoding.

### 3.2 Modelling Strategy
- **Baseline:** Logistic Regression for interpretability and linear relationship capture.
- **Ensemble:** Random Forest Classifier to model complex, non-linear patterns.
- **Evaluation:** Utilized 5-fold cross-validation focusing on **F1-Score** and **ROC-AUC** to ensure model robustness.

### 3.3 Experiment Tracking (MLflow)
Every training run is tracked with **MLflow**:
- **Parameters:** Logged hyperparameters like `max_depth` and `n_estimators`.
- **Metrics:** Tracked Accuracy and AUC-ROC curves.
- **Artifacts:** Serialized model artifacts (`.pkl`) and evaluation plots are versioned and stored.

---

## 4. MLOps: CI/CD & Deployment

### 4.1 CI/CD Pipeline Design
The lifecycle is automated via **GitHub Actions** with the following technical flow:
1.  **Continuous Integration (CI):** Code linting (`flake8`) and unit testing (`pytest`) are triggered on every Pull Request.
2.  **Containerization:** Concurrent Docker builds for high efficiency.
3.  **Infrastructure Automation:** Automated installation of Nginx Ingress Controller and dynamic DNS labeling for the Azure Public IP.
4.  **Continuous Deployment (CD):** Images are pushed to Docker Hub, and Kubernetes manifests are dynamically updated before being applied to the AKS cluster.

### 4.2 Verification Workflow
Post-deployment success can be verified through:
- **Pipeline Logs:** Green status in GitHub Actions for both Build and Deploy stages.
- **Unified Portal:** Accessing all tools (UI, API, Grafana) via the single FQDN.
- **Observability:** Real-time metrics visualization via the Grafana dashboard.

---

## 5. Setup & Repository Access

### 5.1 Local Execution
1. **Clone & Setup:**
   ```bash
   git clone git@github.com:2024ab05112/heart-disease-app.git
   cd heart-disease-app/backend
   python -m venv venv && source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Docker Run:**
   ```bash
   docker-compose up --build
   ```

---
*Generated for MLOps Assignment Submission*
