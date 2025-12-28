from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
from .proxy import proxy_view

urlpatterns = [
    path('', include('webapp.urls')),
    
    # Custom Proxy for Backend API
    # Service Name: heart-disease-service
    path('api/<path:path>', proxy_view, {'upstream_url': 'http://heart-disease-service.default.svc.cluster.local'}),
    path('api/', proxy_view, {'upstream_url': 'http://heart-disease-service.default.svc.cluster.local', 'path': ''}),

    # Custom Proxy for Grafana
    # Service Name: grafana
    path('grafana/<path:path>', proxy_view, {'upstream_url': 'http://grafana.default.svc.cluster.local:3000/grafana'}),
    path('grafana/', proxy_view, {'upstream_url': 'http://grafana.default.svc.cluster.local:3000/grafana', 'path': ''}),

    # Custom Proxy for Prometheus
    # Service Name: prometheus (NOT prometheus-service)
    path('prometheus/<path:path>', proxy_view, {'upstream_url': 'http://prometheus.default.svc.cluster.local:9090/prometheus'}),
    path('prometheus/', proxy_view, {'upstream_url': 'http://prometheus.default.svc.cluster.local:9090/prometheus', 'path': ''}),
]
