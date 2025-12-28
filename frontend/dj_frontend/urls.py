from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
from .proxy import proxy_view

urlpatterns = [
    path('', include('webapp.urls')),
    
    # Custom Proxy for Backend API
    path('api/<path:path>', proxy_view, {'upstream_url': 'http://heart-disease-service'}),
    path('api/', proxy_view, {'upstream_url': 'http://heart-disease-service', 'path': ''}),

    # Custom Proxy for Grafana
    path('grafana/<path:path>', proxy_view, {'upstream_url': 'http://grafana:3000/grafana'}),
    path('grafana/', proxy_view, {'upstream_url': 'http://grafana:3000/grafana', 'path': ''}),

    # Custom Proxy for Prometheus
    path('prometheus/<path:path>', proxy_view, {'upstream_url': 'http://prometheus-service:9090/prometheus'}),
    path('prometheus/', proxy_view, {'upstream_url': 'http://prometheus-service:9090/prometheus', 'path': ''}),
]
