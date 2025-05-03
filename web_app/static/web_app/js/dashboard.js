document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard inicializando...');

    // Definición de colores y configuración común
    const colors = {
        primary: [
            '#F46354', '#36A2EB', '#FFCE56', '#4BC0C0', 
            '#9966FF', '#FF9F40', '#FF99CC', '#66CCFF'
        ],
        background: 'rgba(255, 255, 255, 0.8)'
    };

    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right',
                labels: {
                    font: { size: 12 },
                    padding: 20
                }
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleFont: { size: 14 },
                bodyFont: { size: 13 }
            }
        }
    };

    // Funciones de inicialización de gráficos
    function initializeTypesChart(data) {
        const ctx = document.getElementById('typesChart')?.getContext('2d');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: colors.primary,
                    borderWidth: 1,
                    borderColor: colors.background
                }]
            },
            options: {
                ...commonOptions,
                plugins: {
                    ...commonOptions.plugins,
                    title: {
                        display: true,
                        text: 'Distribución de Tipos de Pokémon',
                        font: { size: 16, weight: 'bold' }
                    }
                }
            }
        });
    }

    function initializeStatsChart(data) {
        const ctx = document.getElementById('statsChart')?.getContext('2d');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['HP', 'Ataque', 'Defensa', 'Atq. Esp.', 'Def. Esp.', 'Velocidad'],
                datasets: [{
                    label: 'Estadísticas Promedio',
                    data: data,
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: '#36A2EB',
                    borderWidth: 2,
                    pointBackgroundColor: '#36A2EB'
                }]
            },
            options: {
                ...commonOptions,
                scales: {
                    r: {
                        beginAtZero: true,
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                },
                plugins: {
                    ...commonOptions.plugins,
                    title: {
                        display: true,
                        text: 'Estadísticas Promedio de Pokémon',
                        font: { size: 16, weight: 'bold' }
                    }
                }
            }
        });
    }

    function initializeExperienceChart(data) {
        const ctx = document.getElementById('experienceChart')?.getContext('2d');
        if (!ctx) return;

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Experiencia Base',
                    data: data.values,
                    backgroundColor: colors.primary[1],
                    borderColor: colors.primary[1],
                    borderWidth: 1
                }]
            },
            options: {
                ...commonOptions,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    ...commonOptions.plugins,
                    title: {
                        display: true,
                        text: 'Top 10 Pokémon por Experiencia',
                        font: { size: 16, weight: 'bold' }
                    }
                }
            }
        });
    }

    try {
        // Verificar que chartData está definido y es válido
        if (typeof chartData === 'undefined') {
            throw new Error('Los datos del gráfico no están definidos');
        }

        console.log('Datos recibidos:', chartData);

        // Inicializar todos los gráficos
        if (chartData.types && chartData.types.labels.length > 0) {
            initializeTypesChart(chartData.types);
        }

        if (chartData.stats && chartData.stats.length > 0) {
            initializeStatsChart(chartData.stats);
        }

        if (chartData.experience && chartData.experience.labels.length > 0) {
            initializeExperienceChart(chartData.experience);
        }

    } catch (error) {
        console.error('Error al inicializar el dashboard:', error);
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger';
        alertDiv.textContent = 'Error al cargar los gráficos. Por favor, recarga la página.';
        document.querySelector('.container-fluid')?.prepend(alertDiv);
    }
});