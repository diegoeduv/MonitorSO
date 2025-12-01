import psutil
from django.shortcuts import render

def dashboard(request):
    cpu_percent = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    procesos = []
    for p in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
        try:
            info = p.info
            procesos.append({
                'pid': info.get('pid'),
                'name': info.get('name') or 'N/A',
                'username': info.get('username') or 'N/A',
                'cpu_percent': info.get('cpu_percent') or 0.0,
                'memory_percent': info.get('memory_percent') or 0.0,
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    # Ordenar por CPU descendente
    procesos = sorted(procesos, key=lambda p: p['cpu_percent'], reverse=True)
    
    procesos = procesos[:20]  # Limitar a los 20 procesos con mayor uso de CPU

    context = {
        'cpu_percent': cpu_percent,
        'mem_total': mem.total,
        'mem_used': mem.used,
        'mem_percent': mem.percent,
        'disk_total': disk.total,
        'disk_used': disk.used,
        'disk_percent': disk.percent,
        'procesos': procesos,
    }

    return render(request, 'monitor/dashboard.html', context)
