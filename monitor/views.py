import psutil
from django.shortcuts import render

def dashboard(request):
    cpu_percent = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    context = {
        'cpu_percent': cpu_percent,
        'mem_total': mem.total,
        'mem_used': mem.used,
        'mem_percent': mem.percent,
        'disk_total': disk.total,
        'disk_used': disk.used,
        'disk_percent': disk.percent,
    }
    return render(request, 'monitor/dashboard.html', context)
