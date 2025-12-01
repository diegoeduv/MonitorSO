// ================== CHARTS CONFIG =================== //

const cpuCtx = document.getElementById('chart_cpu').getContext('2d');
const memCtx = document.getElementById('chart_mem').getContext('2d');
const diskCtx = document.getElementById('chart_disk').getContext('2d');

const chartCPU = new Chart(cpuCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'CPU (%)',
            data: [],
            borderWidth: 2,
            fill: false,
            tension: 0.3
        }]
    },
    options: { scales: { y: { beginAtZero: true, max: 100 } } }
});

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


// ================== FUNCION DE ACTUALIZAR CHARTS =================== //

function updateCharts(cpu, mem, disk) {

    const time = new Date().toLocaleTimeString();

    // CPU
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
