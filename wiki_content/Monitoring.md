# Monitoring Guide (Prometheus & Grafana)

This guide explains how to monitor the health and performance of the Heart Disease Prediction API using the integrated Prometheus and Grafana stack.

## 📊 Overview
- **Prometheus**: Collects metrics from the backend `/metrics` endpoint every 15 seconds.
- **Grafana**: Visualizes these metrics through interactive dashboards.

## 🛠️ Accessing the Dashboards

### 1. FQDN Setup (One-Time)
To access Grafana via `http://grafana.mlops.local`, add the following to your `/etc/hosts` file:

```bash
# Get Minikube IP
minikube ip
# Output example: 192.168.49.2

# Edit hosts file (sudo reqd)
# Add: <minikube-ip> grafana.mlops.local prometheus.mlops.local
sudo nano /etc/hosts
```

### 2. Open Grafana
Go to your browser and visit:  
👉 **http://grafana.mlops.local**

### 3. Login
- **Username**: `admin`
- **Password**: `admin`

> **Note**: A "Heart Disease API Health" dashboard is pre-provisioned for you! No need to create it manually.

### Panel 1: API Request Rate (RPS)
See how many requests your API is handling per second.

-   **Data Source**: Prometheus
-   **Metric Query**: 
    ```promql
    rate(api_requests_total[1m])
    ```
-   **Title**: Requests Per Second
-   **Type**: Time Series

### Panel 2: 95th Percentile Latency
Monitor how fast your API is responding (excluding the slowest 5% of outliers).

-   **Metric Query**:
    ```promql
    histogram_quantile(0.95, rate(api_request_latency_seconds_bucket[5m]))
    ```
-   **Title**: Latency (P95)
-   **Unit**: Seconds (s)

### Panel 3: Endpoint Traffic Distribution
See which API endpoints are being hit (`/predict` vs `/`).

-   **Metric Query**:
    ```promql
    sum(rate(api_requests_total[5m])) by (endpoint)
    ```
-   **Title**: Traffic by Endpoint
-   **Type**: Pie Chart

## 🚨 Troubleshooting
**"No Data" in Graphs?**
1.  Ensure the backend is running and reachable.
2.  Generate some traffic! The metrics only appear after requests are made.
    - Run the frontend and make a few predictions.
    - Or use `curl`:
      ```bash
      minikube service heart-disease-service --url
      # Use the URL returned above
      curl -X POST http://<IP>:<PORT>/predict -d '...'
      ```
3.  Check Prometheus Targets:
    - Open Prometheus: `minikube service prometheus`
    - Go to **Status -> Targets**.
    - Ensure `heart-disease-api` is state **UP**.
