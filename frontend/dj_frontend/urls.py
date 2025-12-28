from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
from .proxy import proxy_view

urlpatterns = [
    path('', include('webapp.urls')),
    
    # Custom Proxy for Backend API
    # Service Name: heart-disease-service
    path('api/<path:path>', proxy_view, {'upstream_url': 'http://heart-disease-service:80'}),
    path('api/', proxy_view, {'upstream_url': 'http://heart-disease-service:80', 'path': ''}),

    # Custom Proxy for Grafana
    # Service Name: grafana
    path('grafana/<path:path>', proxy_view, {'upstream_url': 'http://grafana:3000/grafana'}),
    path('grafana/', proxy_view, {'upstream_url': 'http://grafana:3000/grafana/', 'path': ''}),

    # Custom Proxy for Prometheus
    # Service Name: prometheus
    path('prometheus/<path:path>', proxy_view, {'upstream_url': 'http://prometheus:9090/prometheus'}),
    path('prometheus/', proxy_view, {'upstream_url': 'http://prometheus:9090/prometheus/', 'path': ''}),
]
