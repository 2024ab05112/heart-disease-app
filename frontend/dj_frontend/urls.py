from django.contrib import admin
from django.urls import path, include
from revproxy.views import ProxyView
from django.urls import path, include

urlpatterns = [
    path('', include('webapp.urls')),
    
    # Reverse Proxy for Backend API
    path('api/<path:path>', ProxyView.as_view(upstream='http://heart-disease-service')),
    path('api/', ProxyView.as_view(upstream='http://heart-disease-service')),

    # Reverse Proxy for Grafana
    path('grafana/<path:path>', ProxyView.as_view(upstream='http://grafana:3000/grafana/')),
    path('grafana/', ProxyView.as_view(upstream='http://grafana:3000/grafana/')),

    # Reverse Proxy for Prometheus
    path('prometheus/<path:path>', ProxyView.as_view(upstream='http://prometheus-service:9090/prometheus/')),
    path('prometheus/', ProxyView.as_view(upstream='http://prometheus-service:9090/prometheus/')),
]
