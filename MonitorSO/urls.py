"""
URL configuration for MonitorSO project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from monitor.views import dashboard, api_stats, process_stats, api_specs, api_sensors, api_network, api_gpu

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('api/stats/', api_stats, name='api_stats'),
    path('api/processes/', process_stats, name='process_stats'),
    path("api/specs/", api_specs, name="api_specs"),
    path("api/sensors/", api_sensors, name="api_sensors"),
    path("api/network/", api_network, name="api_network"),
    path("api/gpu/", api_gpu, name="api_gpu"),

]
