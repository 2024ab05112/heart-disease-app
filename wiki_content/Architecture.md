# Service Architecture

This document provides a deep dive into the system's design, covering the data flow, service interactions, and infrastructure components.

## 🏗️ High-Level Architecture

The system is designed as a microservices application deployed on Kubernetes. It separates the user interface (Frontend) from the business logic and inference engine (Backend).

### Visual Workflow (Mermaid)

```mermaid
graph TD
    User([User]) -->|1. Opens Web App| Browser
    
    subgraph K8s_Cluster [Kubernetes Cluster (Minikube)]
        
        subgraph Frontend_Layer [Frontend Layer]
            LB[LoadBalancer / NodePort 30008]
            Django[Django Frontend Pod]
        end
        
        subgraph Backend_Layer [Backend Layer]
            Svc[Backend Service (ClusterIP)]
            FastAPI[FastAPI Backend Pod]
            Model[ML Model (Scikit-Learn)]
        end
        
        User -->|2. Submits Data| LB
        LB -->|Routes| Django
        
        Django -->|3. POST /predict| Svc
        Svc -->|Routes| FastAPI
        
        FastAPI -->|4. Input Validation| FastAPI
        FastAPI -->|5. Run Inference| Model
        Model -- Predictions --> FastAPI
        
        FastAPI -- JSON Response --> Django
        Django -- Rendered HTML --> User
    end
    
    subgraph Observability
        Prometheus[Prometheus] -->|Scrapes Metrics| FastAPI
        Grafana[Grafana] -->|Visualizes| Prometheus
    end
```

### Text-Based Workflow (ASCII)

For quick reference in terminal viewers:

```text
    [ User ]
       |
       | (HTTP Request)
       v
+------------------------+
|   Kubernetes Cluster   |
|                        |
|   +----------------+   |       +-----------------+
|   |  Frontend Pod  |   |       |   Backend Pod   |
|   |    (Django)    |---|------>|    (FastAPI)    |
|   +----------------+   | (JSON)|   (ML Model)    |
|           ^            |       +-----------------+
|           |            |               |
|   +-------+--------+   |               |
|   | Output Display |<--|---------------|
|   +----------------+   |
+------------------------+
```

## 🔍 Component Breakdown

### 1. Frontend Service (Django)
- **Role**: Serves the user interface and handles user interactions.
- **Port**: Exposed externally on port `30008` (NodePort).
- **Function**: Accepts patient data via a web form, serializes it, and sends it to the backend. It then renders the prediction result for the user.

### 2. Backend Service (FastAPI)
- **Role**: Provides the REST API for model inference.
- **Port**: Internal ClusterIP service on port `80`.
- **Function**: 
    - Loads the trained Scikit-Learn model at startup.
    - Validates input data using Pydantic models.
    - Generates predictions and confidence scores.
    - Exposes Prometheus metrics at `/metrics`.

### 3. Monitoring Stack
- **Prometheus**: Scrapes performance metrics (request latency, generic health) from the backend.
- **Grafana**: Visualizes these metrics on dashboards for system health monitoring.

## 🔄 Data Flow Scenario

1. **Input**: User enters "Age: 45, Cholesterol: 250..." in the UI.
2. **Processing**: Frontend sends this as a JSON payload to `http://heart-disease-service/predict`.
3. **Inference**: Backend converts JSON to a DataFrame, passes it to `model.predict()`.
4. **Output**: Backend returns `{"prediction": 1, "confidence": 0.85}`.
5. **Display**: Frontend shows "Heart Disease Detected (85% Confidence)".
