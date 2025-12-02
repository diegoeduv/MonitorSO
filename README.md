# MonitorSO

Dashboard de monitorización del sistema operativo desarrollado en Django. La aplicación muestra métricas en tiempo real (CPU, memoria, disco, GPU, red, temperaturas y procesos) utilizando `psutil` y otros módulos opcionales para GPU.

## Características

- Métricas de CPU, RAM, disco y GPU
- Temperaturas de CPU/GPU
- Actividad de red (velocidad de transferencia)
- Gráficas en tiempo real con Chart.js
- Listado de procesos (más pesados)
- Actualizaciones dinámicas cada 2 segundos mediante `fetch`    
- Interfaz modularizada en componentes HTML, CSS y JavaScript

## Estructura del proyecto

```
MonitorSO/
├── monitor/
│   ├── static/monitor/
│   │   ├── css/monitor.css
│   │   └── js/
│   │       ├── monitor_charts.js
│   │       └── monitor_updates.js
│   ├── templates/monitor/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   └── components/
│   │       ├── card_cpu.html
│   │       ├── card_mem.html
│   │       ├── card_disk.html
│   │       ├── card_gpu.html
│   │       ├── temperaturas.html
│   │       ├── red.html
│   │       ├── graficas.html
│   │       ├── especificaciones.html
│   │       └── procesos.html
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── filters.py
│   ├── views.py
│   └── urls.py
├── MonitorSO/
│   ├── settings.py
│   └── urls.py
└── manage.py
```

## Instalación

1. Clona el repositorio

```bash
git clone https://github.com/tuusuario/MonitorSO.git
cd MonitorSO
```

2. Crea y activa un entorno virtual

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
```

3. Instala dependencias

```bash
pip install -r requirements.txt
```

4. Aplica migraciones

```bash
python manage.py migrate
```

5. Ejecuta el servidor de desarrollo

```bash
python manage.py runserver
```

Accede a `http://127.0.0.1:8000/` en tu navegador.

## Dependencias

- `Django`
- `psutil`

Dependencias opcionales para monitorización de GPU:

- `nvidia-ml-py` (NVIDIA)
- `pyamdgpuinfo` (AMD)

## Funcionamiento

La aplicación utiliza Django para renderizar las vistas y JavaScript (Fetch API) para solicitar datos al backend en intervalos regulares (2s). Los endpoints de la API devuelven JSON con las métricas necesarias para actualizar los componentes y gráficas.

### Datos que se actualizan

- Porcentaje de CPU y gráfica histórica
- Porcentaje y uso de memoria (GB)
- Uso de disco
- Uso de GPU y VRAM
- Velocidad de red (upload/download)
- Temperaturas de sensores
- Lista de procesos ordenada por uso de recursos

## Endpoints

| Endpoint | Descripción |
|---|---|
| `/api/stats/` | CPU, memoria y disco |
| `/api/processes/` | Top procesos (ej. 20 más pesados) |
| `/api/specs/` | Especificaciones del sistema |
| `/api/sensors/` | Temperaturas de CPU/GPU |
| `/api/network/` | Velocidad/estadísticas de red |
| `/api/gpu/` | Estado y métricas de GPU |

Todos los endpoints devuelven JSON.

Ejemplo de respuesta para `/api/stats/`:

```json
{
  "cpu_percent": 34.5,
  "mem_percent": 62.1,
  "mem_used": 8343216128,
  "disk_percent": 55.9,
  "disk_used": 72243781632
}
```

## Frontend

El frontend está dividido en componentes dentro de `templates/monitor/components/`. El archivo `dashboard.html` incluye estos componentes y los scripts en `static/monitor/js/` manejan las gráficas (`monitor_charts.js`) y las actualizaciones (`monitor_updates.js`).

Ejemplo de inclusión en `dashboard.html`:

```django
{% include "monitor/components/card_cpu.html" %}
{% include "monitor/components/card_mem.html" %}
```

## Filtros personalizados

La aplicación incluye un filtro `to_gb` en `monitor/templatetags/filters.py`:

```django
{{ mem_total|to_gb }}
```

## Tecnologías

- Python 3
- Django
- psutil
- Chart.js
- Bootstrap
- Fetch API
