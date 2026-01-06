# Service Architecture & Workflow

This document details the architecture and request flow of the Heart Disease Prediction System.

## Architecture Diagram

The following Mermaid diagram illustrates how the different components interact within the Kubernetes cluster using dedicated Load Balancers.

```mermaid
graph TD
    subgraph Users [Users / External]
        U1([User Accessing Web UI])
        U2([Dev Accessing API Docs])
        U3([Admin Accessing Grafana])
    end

    subgraph Azure_LoadBalancers [Azure Load Balancers]
        LB_Fnd[Frontend LB]
        LB_API[API LB]
        LB_GF[Grafana LB]
        LB_PR[Prometheus LB]
    end

    subgraph K8s_Cluster [AKS Cluster]
        
        subgraph Frontend_Group [Frontend Layer]
            Django[Django App]
        end
        
        subgraph Backend_Group [Backend Layer]
            FastAPI[FastAPI Service]
            MLModel[ML Model]
        end
        
        subgraph Monitoring_Group [Observability Layer]
            Prometheus[Prometheus Server]
            Grafana[Grafana Dashboards]
        end

        %% Connections
        LB_Fnd --> Django
        LB_API --> FastAPI
        LB_GF --> Grafana
        LB_PR --> Prometheus

        Django -->|Synchronous POST| Backend_Svc[Internal API Service]
        Backend_Svc --> FastAPI
        FastAPI -->|Inference| MLModel
        Prometheus -->|Scrapes| Backend_Svc
        Grafana -->|Queries| Prometheus
    end

    U1 --> LB_Fnd
    U2 --> LB_API
    U3 --> LB_GF
```

## Service Communication Details

### 1. External Access Points
Each service is reachable via a unique Azure DNS label under the `centralindia.cloudapp.azure.com` domain.

- **Frontend:** `heart-disease-2024ab05112`
- **Backend API:** `heart-disease-api-2024ab05112`
- **Grafana:** `heart-disease-grafana-2024ab05112`
- **Prometheus:** `heart-disease-prom-2024ab05112`

### 2. Frontend -> Backend (Internal)
- **Service**: `heart-disease-service`
- **Type**: LoadBalancer (Internal IP)
- **Internal DNS**: `heart-disease-service`
- **Flow**:
    - When a user submits the form, the Django view sends a synchronous HTTP POST request to `http://heart-disease-service:80/api/predict`.
    - This communication stays **inside** the cluster network for maximum performance and security.

### 3. Backend Execution
- The FastAPI application receives the request payload.
- It loads the pre-trained model and performs inference.
- Results are returned as JSON, which Django then renders for the user.

### 4. Monitoring Flow
- **Prometheus** scrapes metrics directly from the backend service at `http://heart-disease-service:80/api/metrics`.
- **Grafana** is configured with an internal datasource pointing to `http://prometheus:9090`.
- Users can access the Grafana UI directly to view the "Heart Disease API Health" dashboard without passing through the Django frontend.
