import platform
import shutil
import subprocess
import time

import psutil
from django.http import JsonResponse
from django.shortcuts import render


GPU_CHECKED = False
GPU_INFO_CACHED = None


# Devuelve estadísticas básicas del sistema
def api_stats(request):
    cpu_percent = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return JsonResponse({
        "cpu_percent": cpu_percent,
        "mem_used": mem.used,
        "mem_percent": mem.percent,
        "disk_used": disk.used,
        "disk_percent": disk.percent,
    })


# Devuelve los 20 procesos que más CPU consumen
def process_stats(request):
    cpu_cores = psutil.cpu_count(logical=True) or 1
    procesos = []

    for p in psutil.process_iter([
        'pid', 'name', 'username', 'cpu_percent', 'memory_percent'
    ]):
        try:
            info = p.info
            cpu_raw = info.get("cpu_percent") or 0.0

            procesos.append({
                "pid": info.get("pid"),
                "name": info.get("name") or "N/A",
                "username": info.get("username") or "N/A",
                "cpu_percent": cpu_raw / cpu_cores,
                "memory_percent": info.get("memory_percent") or 0.0,
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    procesos = sorted(
        procesos,
        key=lambda p: p["cpu_percent"],
        reverse=True
    )[:20]

    return JsonResponse({"procesos": procesos})


# Detecta si existe alguna GPU y la guarda en caché
def gpu_exists():
    global GPU_CHECKED, GPU_INFO_CACHED

    if GPU_CHECKED:
        return GPU_INFO_CACHED

    system = platform.system()

    # NVIDIA
    nvidia_smi = shutil.which("nvidia-smi")
    if nvidia_smi:
        try:
            output = subprocess.check_output(
                [nvidia_smi, "--query-gpu=name", "--format=csv,noheader"],
                stderr=subprocess.STDOUT
            ).decode().strip()

            GPU_INFO_CACHED = {
                "exists": True,
                "vendor": "NVIDIA",
                "model": output.splitlines()[0].strip(),
            }
            GPU_CHECKED = True
            return GPU_INFO_CACHED

        except Exception:
            pass

    # AMD vía sensores
    if system == "Linux":
        temps = psutil.sensors_temperatures()
        if "amdgpu" in temps:
            GPU_INFO_CACHED = {
                "exists": True,
                "vendor": "AMD",
                "model": "AMD GPU (detected via sensors)",
            }
            GPU_CHECKED = True
            return GPU_INFO_CACHED

    # Intel vía lspci
    if system == "Linux":
        try:
            lspci = subprocess.check_output(["lspci"]).decode().lower()
            if "intel" in lspci and "vga" in lspci:
                GPU_INFO_CACHED = {
                    "exists": True,
                    "vendor": "Intel",
                    "model": "Intel Integrated GPU",
                }
                GPU_CHECKED = True
                return GPU_INFO_CACHED
        except Exception:
            pass

    GPU_INFO_CACHED = {"exists": False, "vendor": None, "model": None}
    GPU_CHECKED = True
    return GPU_INFO_CACHED


# Obtiene información avanzada de la GPU si existe
def gpu_info():
    gpu = gpu_exists()
    if not gpu["exists"]:
        return None

    # NVIDIA
    if gpu["vendor"] == "NVIDIA":
        try:
            out = subprocess.check_output([
                "nvidia-smi",
                "--query-gpu=name,memory.total,memory.used,utilization.gpu,temperature.gpu",
                "--format=csv,noheader,nounits",
            ]).decode().strip()

            name, mem_total, mem_used, util, temp = [
                x.strip() for x in out.split(",")
            ]

            return {
                "name": name,
                "memory_total": int(mem_total),
                "memory_used": int(mem_used),
                "utilization": int(util),
                "temperature": int(temp),
            }

        except Exception:
            return None

    # AMD
    if gpu["vendor"] == "AMD":
        temps = psutil.sensors_temperatures()
        gpu_temps = temps.get("amdgpu", [])
        if gpu_temps:
            return {
                "name": "AMD GPU",
                "temperature": gpu_temps[0].current,
                "memory_total": None,
                "memory_used": None,
                "utilization": None,
            }

    return None


# Devuelve especificaciones del sistema
def api_specs(request):
    g = gpu_exists()
    cpu_freq = psutil.cpu_freq()

    # RAM y SWAP
    ram = psutil.virtual_memory()
    swap = psutil.swap_memory()

    # Disco principal
    disk = psutil.disk_usage("/")

    return JsonResponse({
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "hostname": platform.node(),

        "cpu_name": platform.processor(),
        "cpu_physical_cores": psutil.cpu_count(logical=False),
        "cpu_logical_cores": psutil.cpu_count(logical=True),

        "cpu_freq_current": cpu_freq.current if cpu_freq else None,
        "cpu_freq_min": cpu_freq.min if cpu_freq else None,
        "cpu_freq_max": cpu_freq.max if cpu_freq else None,

        "gpu_exists": g["exists"],
        "gpu_vendor": g["vendor"],
        "gpu_name": g["model"],

        # NUEVO → RAM / SWAP
        "ram_total": ram.total,
        "swap_total": swap.total,

        # NUEVO → DISCO
        "disk_total": disk.total,
    })



# Devuelve temperaturas de CPU y GPU
def api_sensors(request):
    temps = psutil.sensors_temperatures()
    cpu_temps = temps.get("coretemp", temps.get("cpu-thermal", []))

    cpu_temp = None
    if cpu_temps:
        cpu_temp = sum(t.current for t in cpu_temps) / len(cpu_temps)

    gpu = gpu_info()
    gpu_temp = gpu.get("temperature") if gpu else None

    return JsonResponse({
        "cpu_temperature": cpu_temp,
        "gpu_temperature": gpu_temp,
    })


# Devuelve información de la GPU para el dashboard
def api_gpu(request):
    gpu = gpu_info()
    if not gpu:
        return JsonResponse({"exists": False})

    return JsonResponse({
        "exists": True,
        "name": gpu.get("name"),
        "memory_total": gpu.get("memory_total"),
        "memory_used": gpu.get("memory_used"),
        "utilization": gpu.get("utilization"),
    })


# Renderiza la vista principal del dashboard
def dashboard(request):
    cpu_percent = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    procesos = []
    for p in psutil.process_iter([
        'pid', 'name', 'username', 'cpu_percent', 'memory_percent'
    ]):
        try:
            info = p.info
            procesos.append({
                "pid": info.get("pid"),
                "name": info.get("name") or "N/A",
                "username": info.get("username") or "N/A",
                "cpu_percent": info.get("cpu_percent") or 0.0,
                "memory_percent": info.get("memory_percent") or 0.0,
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    procesos = sorted(
        procesos, key=lambda p: p["cpu_percent"], reverse=True
    )[:20]

    context = {
        "cpu_percent": cpu_percent,
        "mem_total": mem.total,
        "mem_used": mem.used,
        "mem_percent": mem.percent,
        "disk_total": disk.total,
        "disk_used": disk.used,
        "disk_percent": disk.percent,
        "procesos": procesos,
    }

    return render(request, "monitor/dashboard.html", context)


last_net = psutil.net_io_counters()
last_time = time.time()


# Devuelve velocidad de subida y bajada en tiempo real
def api_network(request):
    global last_net, last_time

    now = time.time()
    new_net = psutil.net_io_counters()

    elapsed = now - last_time
    sent_per_sec = (new_net.bytes_sent - last_net.bytes_sent) / elapsed
    recv_per_sec = (new_net.bytes_recv - last_net.bytes_recv) / elapsed

    last_net = new_net
    last_time = now

    return JsonResponse({
        "upload": sent_per_sec,
        "download": recv_per_sec,
    })
