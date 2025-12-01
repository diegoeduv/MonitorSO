// Charts de uso del sistema: inicialización de gráficos (CPU, Memoria, Disco)

const cpuCtx = document.getElementById('chart_cpu').getContext('2d');
const memCtx = document.getElementById('chart_mem').getContext('2d');
const diskCtx = document.getElementById('chart_disk').getContext('2d');

// Gráfico de CPU
const chartCPU = new Chart(cpuCtx, {
    type: 'line',
    data: {
        labels: [], // Tiempos de muestreo
        datasets: [{
            label: 'CPU (%)',
            data: [], // Valores de CPU
            borderWidth: 2,
            fill: false,
            tension: 0.3 // Suavizado de la línea
        }]
    },
    options: { scales: { y: { beginAtZero: true, max: 100 } } }
});

// Gráfico de Memoria
const chartMEM = new Chart(memCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Memoria (%)',
            data: [],
            borderWidth: 2,
            fill: false,
            tension: 0.3
        }]
    },
    options: { scales: { y: { beginAtZero: true, max: 100 } } }
});

// Gráfico de Disco
const chartDISK = new Chart(diskCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Disco (%)',
            data: [],
            borderWidth: 2,
            fill: false,
            tension: 0.3
        }]
    },
    options: { scales: { y: { beginAtZero: true, max: 100 } } }
});



// Función para actualizar los gráficos en tiempo real
function updateCharts(cpu, mem, disk) {

    const time = new Date().toLocaleTimeString(); // Etiqueta de tiempo

    // CPU: agrega dato y mantiene máximo 20 puntos
    chartCPU.data.labels.push(time);
    chartCPU.data.datasets[0].data.push(cpu);
    if (chartCPU.data.labels.length > 20) {
        chartCPU.data.labels.shift();
        chartCPU.data.datasets[0].data.shift();
    }
    chartCPU.update();

    // Memoria
    chartMEM.data.labels.push(time);
    chartMEM.data.datasets[0].data.push(mem);
    if (chartMEM.data.labels.length > 20) {
        chartMEM.data.labels.shift();
        chartMEM.data.datasets[0].data.shift();
    }
    chartMEM.update();

    // Disco
    chartDISK.data.labels.push(time);
    chartDISK.data.datasets[0].data.push(disk);
    if (chartDISK.data.labels.length > 20) {
        chartDISK.data.labels.shift();
        chartDISK.data.datasets[0].data.shift();
    }
    chartDISK.update();
}
