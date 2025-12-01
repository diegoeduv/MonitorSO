// ============== FUNCIONES UTILIDADES ============== //

function toGB(bytes) {
    return (bytes / (1024 ** 3)).toFixed(2) + " GB";
}

function formatSpeed(bytes) {
    if (bytes < 1024) return bytes.toFixed(0) + " B/s";
    if (bytes < 1024 ** 2) return (bytes / 1024).toFixed(1) + " KB/s";
    return (bytes / 1024 / 1024).toFixed(1) + " MB/s";
}


// ============== ESTADISTICAS (CPU/MEM/DISKO) ============== //

async function updateStats() {
    const res = await fetch("/api/stats/");
    const data = await res.json();

    // CPU
    document.getElementById("cpu_val").innerText = data.cpu_percent + "%";
    document.getElementById("cpu-bar").style.width = data.cpu_percent + "%";

    // Memoria
    document.getElementById("mem_val").innerText = data.mem_percent + "%";
    document.getElementById("mem_bar");
    document.getElementById("mem-bar").style.width = data.mem_percent + "%";
    document.getElementById("mem_used").innerText = toGB(data.mem_used);

    // Disco
    document.getElementById("disk_val").innerText = data.disk_percent + "%";
    document.getElementById("disk-bar").style.width = data.disk_percent + "%";
    document.getElementById("disk_used").innerText = toGB(data.disk_used);

    // Update charts
    updateCharts(data.cpu_percent, data.mem_percent, data.disk_percent);
}

setInterval(updateStats, 2000);


// ============== PROCESOS ============== //

async function updateProcesses() {
    const res = await fetch("/api/processes/");
    const data = await res.json();

    const tbody = document.getElementById("process_body");
    tbody.innerHTML = "";

    data.procesos.forEach((p, index) => {
        const row = `
        <tr>
            <td>${index + 1}</td>
            <td class="pid-cell">${p.pid}</td>
            <td class="name-cell">${p.name}</td>
            <td class="user-cell">${p.username}</td>
            <td>
                <div class="metric">
                    <span class="metric-value">${p.cpu_percent.toFixed(1)}%</span>
                    <div class="metric-bar">
                        <div class="metric-bar-fill" style="width: ${p.cpu_percent}%;"></div>
                    </div>
                </div>
            </td>
            <td>
                <div class="metric">
                    <span class="metric-value">${p.memory_percent.toFixed(1)}%</span>
                    <div class="metric-bar">
                        <div class="metric-bar-fill" style="width: ${p.memory_percent}%;"></div>
                    </div>
                </div>
            </td>
        </tr>
        `;
        tbody.innerHTML += row;
    });
}

setInterval(updateProcesses, 2000);


// ============== SENSORES (TEMPERATURAS) ============== //

async function updateSensors() {
    const res = await fetch("/api/sensors/");
    const data = await res.json();

    document.getElementById("cpu_temp").innerText =
        data.cpu_temperature ? data.cpu_temperature.toFixed(1) + "°C" : "N/A";

    document.getElementById("gpu_temp").innerText =
        data.gpu_temperature ? data.gpu_temperature + "°C" : "N/A";
}

setInterval(updateSensors, 2000);


// ============== RED ============== //

async function updateNetwork() {
    const res = await fetch("/api/network/");
    const data = await res.json();

    document.getElementById("net_up").innerText = formatSpeed(data.upload);
    document.getElementById("net_down").innerText = formatSpeed(data.download);
}

setInterval(updateNetwork, 2000);


// ============== GPU ============== //

async function updateGPU() {
    const res = await fetch("/api/gpu/");
    const data = await res.json();

    if (!data.exists) {
        document.getElementById("gpu_name_box").innerText = "No detectada";
        document.getElementById("gpu_util_percent").innerText = "N/A";
        document.getElementById("gpu_bar").style.width = "0%";
        document.getElementById("gpu_mem_box").innerText = "-";
        return;
    }

    document.getElementById("gpu_name_box").innerText = data.name;

    if (data.utilization !== null) {
        document.getElementById("gpu_util_percent").innerText = data.utilization + "%";
        document.getElementById("gpu_bar").style.width = data.utilization + "%";
    }

    if (data.memory_total !== null) {
        document.getElementById("gpu_mem_box").innerText =
            `${data.memory_used} / ${data.memory_total} MB`;
    }
}

setInterval(updateGPU, 2000);


// ============== ESPECIFICACIONES ============== //

async function loadSpecs() {
    const res = await fetch("/api/specs/");
    const data = await res.json();

    // Sistema
    document.getElementById("spec_os").innerText = data.os;
    document.getElementById("spec_os_version").innerText = data.os_version;
    document.getElementById("spec_hostname").innerText = data.hostname;
    document.getElementById("spec_machine").innerText = data.machine;

    // CPU
    document.getElementById("spec_cpu_name").innerText = data.cpu_name;
    document.getElementById("spec_cpu_phys").innerText = data.cpu_physical_cores;
    document.getElementById("spec_cpu_logical").innerText = data.cpu_logical_cores;
    document.getElementById("spec_cpu_freq").innerText =
        data.cpu_freq_current ? data.cpu_freq_current.toFixed(0) + " MHz" : "N/A";

    // RAM
    document.getElementById("spec_ram").innerText = toGB(data.ram_total);
    document.getElementById("spec_swap").innerText = toGB(data.swap_total);

    // Disco
    document.getElementById("spec_disk").innerText = toGB(data.disk_total);

    // GPU
    if (data.gpu_exists) {
        document.getElementById("spec_gpu_name").innerText = data.gpu_name;
        document.getElementById("spec_gpu_vendor").innerText = data.gpu_vendor;
    } else {
        document.getElementById("spec_gpu_name").innerText = "No detectada";
        document.getElementById("spec_gpu_vendor").innerText = "-";
    }
}

loadSpecs();
