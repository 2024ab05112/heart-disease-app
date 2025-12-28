# Comprehensive MLOps Project Documentation
## Heart Disease Prediction System

**Author:** 2024ab05112  
**Date:** December 29, 2024  
**Project Role:** MLOps Engineer / Full Stack Developer  

---

## **1. Introduction**

### **1.1. Project Overview**
The **Heart Disease Prediction System** is an end-to-end Machine Learning Operations (MLOps) project designed to predict the likelihood of heart disease in patients based on clinical parameters (e.g., age, cholesterol, blood pressure). 

Unlike a simple notebook application, this project demonstrates a **production-grade architecture** where the model is served as a scalable microservice, consumed by a user-friendly web interface, and orchestrated using **Kubernetes** on **Azure Cloud**.

### **1.2. Key Objectives**
- **Automated Deployment**: Implement a CI/CD pipeline to automatically build and deploy changes.
- **Microservices Architecture**: Decouple the ML inference logic (Backend) from the User Interface (Frontend).
- **Scalability**: Use Kubernetes (AKS) to manage containerized applications.
- **Observability**: Integrate Prometheus and Grafana for real-time system monitoring.
- **Cloud Native**: Leverage Cloud-native patterns (LoadBalancers, DNS) for public access.

---

## **2. Dataset and Modeling**

### **2.1. Dataset Description**
The project uses the "Heart Disease UCI" dataset, a standard benchmark for binary classification problems in healthcare.

*   **Source**: UCI Machine Learning Repository / Kaggle.
*   **Features**: 13 predictive attributes + 1 target variable.
    *   `age`: Age in years.
    *   `sex`: (1 = male; 0 = female).
    *   `cp`: Chest pain type (4 values).
    *   `trestbps`: Resting blood pressure.
    *   `chol`: Serum cholestoral in mg/dl.
    *   `fbs`: Fasting blood sugar > 120 mg/dl.
    *   `restecg`: Resting electrocardiographic results.
    *   `thalach`: Maximum heart rate achieved.
    *   `exang`: Exercise induced angina.
    *   `oldpeak`: ST depression induced by exercise relative to rest.
    *   `slope`: The slope of the peak exercise ST segment.
    *   `ca`: Number of major vessels (0-3) colored by flourosopy.
    *   `thal`: 3 = normal; 6 = fixed defect; 7 = reversable defect.
*   **Target**: `target` (1 = Heart Disease Presence, 0 = Absence).

### **2.2. Exploratory Data Analysis (EDA)**
Before training, intensive data exploration was performed to understand feature distributions.
*   **Correlation Matrix**: Identified key drivers like `cp` (chest pain) and `thalach` (max heart rate).
*   **Class Balance**: Verified that the dataset was balanced enough to avoid major bias.

### **2.3. Model Training & Evaluation**
The model was built using **Scikit-Learn** and tracked with **MLflow**.

*   **Algorithms Tested**: 
    1.  *Logistic Regression*: Baseline linear model.
    2.  *Random Forest Classifier*: selected for final deployment due to higher accuracy (~85%).
*   **Artifacts**: The trained model is serialized as a Python pickle object (`model.pkl` or MLflow artifact) and packaged inside the Docker container.
*   **Input Validation**: Code ensures inputs match the schema (e.g., `sex` must be 0 or 1).

---

## **3. Application Architecture**

The system follows a microservices pattern with two distinct components communicating over a private Kubernetes network.

### **3.1. Architecture Diagram**

```text
    [ Internet ]
         |
         v
[ Azure LoadBalancer ] (Public IP / DNS)
         |
         v
+------------------------+
|   Kubernetes Cluster   |
|                        |
|   +----------------+   | HTTP (JSON)  +-----------------+
|   |  Frontend Pod  |---|------------->|   Backend Pod   |
|   | (Django App)   |   |              |  (FastAPI App)  |
|   +-------+--------+   |              +--------+--------+
|           ^            |                       |
|           |            |              +--------v--------+
|           |            |              |    ML Model     |
|       (UI View)        |              +-----------------+
+------------------------+
```

### **3.2. Backend Service (FastAPI)**
The core logic resides in `backend/src/app.py`.
*   **Framework**: FastAPI (High performance, auto-documentation).
*   **Endpoint**: `POST /api/predict`
    *   Accepts a JSON payload fitting the `PatientInput` Pydantic model.
    *   Returns `{"prediction": 1, "confidence": 0.85}`.
*   **Metrics**: Exposes `/api/metrics` for Prometheus scraping (Request Count, Latency).

### **3.3. Frontend Service (Django)**
The user interface is in `frontend/webapp/views.py`.
*   **Framework**: Django (Robust, MTV architecture).
*   **Function**:
    *   Renders an HTML form (`index.html`) for data entry.
    *   On submission, validates form data.
    *   Sends a synchronous HTTP POST request to the internal backend URL: `http://heart-disease-service:80/api/predict`.
    *   Displays the result vividly (Red for Danger, Green for Safe).
*   **Configuration**: Uses Django's `requests` library to bridge the gap to the backend.

---

## **4. Infrastructure & Deployment**

### **4.1. Docker Containerization**
Both services are containerized to ensure consistency across environments.
*   **Backend Image**: `2024ab05112/heart-disease-api`
    *   Base: `python:3.9-slim`
    *   Installs dependencies from `requirements.txt`.
    *   Copies trained model artifacts.
*   **Frontend Image**: `2024ab05112/heart-disease-frontend`
    *   Base: `python:3.9-slim`
    *   Runs Django Development server (migrating to Gunicorn for production recommended).

### **4.2. Kubernetes Configuration (AKS)**
The application runs on **Azure Kubernetes Service (AKS)**.

1.  **Deployments**:
    *   `backend-deployment.yml`: One replica of the API.
    *   `frontend-deployment.yml`: One replica of the UI.
2.  **Services**:
    *   `heart-disease-service` (ClusterIP): Internal only. Allows Frontend to find Backend.
    *   `heart-disease-frontend-service` (LoadBalancer): **Publicly exposed**.
3.  **DNS & Routing**:
    *   The frontend service uses an Azure annotation: `service.beta.kubernetes.io/azure-dns-label-name: heart-disease-2024ab05112`.
    *   This maps the dynamic Public IP to a stable FQDN: `heart-disease-2024ab05112.eastus.cloudapp.azure.com`.

---

## **5. CI/CD Pipeline (GitHub Actions)**

The project utilizes a strict DevOps workflow defined in `.github/workflows/deploy.yml`.

### **5.1. Workflow Triggers**
*   **Push to Main**: Code updates automatically trigger the pipeline.
*   **Path Filtering**: "Smart Build" logic ensures that backend tests/builds only run if `backend/` code changes.

### **5.2. Pipeline Stages**
1.  **Check Changes**: Identifies which microservices were modified.
2.  **Build & Push**:
    *   Builds Docker images.
    *   Tags them with the unique Git Commit SHA (e.g., `image:a1b2c3d`).
    *   Pushes to Docker Hub.
3.  **Start Environment**:
    *   Checks if the AKS cluster (`HeartDiseaseCluster`) is Stopped.
    *   If Stopped, executes `az aks start` to provision resources on-demand.
4.  **Deploy**:
    *   Patches the Kubernetes manifests with the *new* image tags.
    *   Executes `kubectl apply` to roll out updates without downtime.

---

## **6. Monitoring & Observability**

### **6.1. Prometheus**
*   Deployed in the cluster to scrape metrics.
*   Target: `heart-disease-service:80/metrics`.
*   Metrics Collected:
    *   `prediction_request_count_total`: Traffic volume.
    *   `prediction_request_latency_seconds`: API performance speed.

### **6.2. Grafana**
*   Visualizes the metrics collected by Prometheus.
*   Dashboards provide insights into system health and real-time usage (e.g., "Requests per Minute").

---

## **7. Testing & Validation**

### **7.1. How to Run Integration Tests (Manual)**
1.  **Push Code**: Commit a change to GitHub.
2.  **Monitor Pipeline**: verifying all 3 stages (Build, Infra Start, Deploy) pass.
3.  **Access URL**: Visit `http://heart-disease-2024ab05112.eastus.cloudapp.azure.com`.
4.  **Submit Form**: Enter valid patient data.
    *   *Example*: Age 60, Cholesterol 300 (High Risk parameters).
5.  **Verify Output**: Ensure the UI returns a prediction result.

### **7.2. Troubleshooting**
*   **500 Error**: Usually indicates the Backend is unreachable. Check `kubectl get pods` to see if backend crashed.
*   **404 Error**: Check if the URL path in `views.py` matches `app.py`.

---

## **8. Conclusion**
This project successfully demonstrates the modernization of a Machine Learning workload. By moving from a static notebook to a dynamic, cloud-native microservices architecture, we achieved:
1.  **Reliability**: Automated pipelines reduce human error.
2.  **Scalability**: Kubernetes handles load efficiently.
3.  **Accessibility**: The model is now available to anyone via a web URL.
4.  **Visibility**: Monitoring tools provide constant insight into model performance.

---
**End of Document**
