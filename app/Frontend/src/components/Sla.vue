<script setup>
import { onMounted, ref, computed, watch } from 'vue';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

// Get the logs and estimated hours from props
const props = defineProps({
    logged_hrs: {
        type: Array,
        required: true
    },
    estimated_hrs: {
        type: Number,
        required: true
    }

});


// const loggs = computed(() => props.logged_hrs);
const loggs = computed(() => props.logged_hrs);
const estimated_hrs = computed(() => props.estimated_hrs);
const esthours = ref(0);

let perscent_sla = ref(0);
let sprintChart = ref(null);
const sprintChartRef = ref(null);

const updateSLA = () => {
    const totalLogged = loggs.value && loggs.value.length > 0
        ? loggs.value.reduce((acc, log) => acc + parseInt(log.logged || 0, 10), 0)
        : 0; // Fallback to 0 if no logs
    
    perscent_sla.value = (totalLogged / esthours.value) * 100;
    if (isNaN(perscent_sla.value)) {
        perscent_sla.value = 0; // Fallback to 0 if the result is NaN
    }
};

import { watchEffect } from 'vue';

function update_est(){
    updateSLA();
}

watchEffect(() => {
    // Ensure data is available before drawing the chart
    if (loggs.value.length > 0) {
        esthours.value = estimated_hrs.value;
        updateSLA();
        console.log('Initial logged hours:', loggs.value);
    }
});

onMounted(() => {
    console.log('Initial logged hours:', loggs.value);
    // updateSLA();
    // drawSprintChart();
    setTimeout(() => {
        drawSprintChart();
    }, 1000);
});



function drawSprintChart() {
    if (!loggs.value || loggs.value.length === 0) {
        console.warn('No logged hours data available for the chart.');
        return; // Exit if there’s no data
    }

    const ctx = sprintChartRef.value.getContext('2d');

    if (!ctx) {
        console.error("Canvas context is null. Ensure the canvas element exists.");
        return;
    }

    const daysInMonth = new Date(new Date().getFullYear(), new Date().getMonth() + 1, 0).getDate();
    let labels = Array.from({ length: daysInMonth }, (_, i) => i + 1);
    let data = Array.from({ length: daysInMonth }, () => 0); // Initialize with 0
    console.log('Data:', data);
    // Check the log data and parse it correctly
    loggs.value.forEach(log => {
        let logDate = new Date(log.date);
        if (!isNaN(logDate.getTime())) { // Ensure logDate is valid
            let day = logDate.getDate();
            // Parse logged hours correctly
            let loggedHours = parseInt(log.logged);
            if (!isNaN(loggedHours)) { // Check if loggedHours is a valid number
                data[day - 1] += loggedHours; // Accumulate logged hours
            } else {
                console.warn(`Invalid logged hours: ${log.logged}`);
            }
        } else {
            console.warn(`Invalid date: ${log.date}`);
        }
    });

    // Destroy previous chart instance if exists
    if (sprintChart.value) {
        sprintChart.value.destroy();
    }

    // Create a new chart instance
    sprintChart.value = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Logged Hours',
                data: data,
                fill: true,
                backgroundColor: 'rgba(39, 162, 149, 0.7)',
                borderColor: '#27a295',
                borderWidth: 1,
                pointRadius: 4,
                tension: 0.31,
                pointBackgroundColor: '#27a295',
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                    enabled: true
                }
            },
            scales: {
                x: {
                    display: true,
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#666',
                        font: {
                            size: 6
                        }
                    },
                },
                y: {
                    display: true,
                    grid: {
                        display: false,
                    },
                    ticks: {
                        color: '#666',
                        font: {
                            size: 6
                        }
                    },
                    beginAtZero: true,
                }
            },
            elements: {
                line: {
                    tension: 0.1
                }
            },
            maintainAspectRatio: false,
            responsive: true
        }
    });
}

</script>

<template>
    <div class="sla-container">
        <div class="sla_text">Time to SLA</div>
        <div class="progress">
            <div class="progress-bar" role="progressbar" :style="{ width: perscent_sla + '%' }">
            </div>
        </div>
        <input class="numbner_sla" type="number" v-model="esthours" @change="update_est" />
        <!-- <div class="sla_text">{{ loggs.reduce((acc, log) => acc + parseInt(log.logged), 0) }} / {{ estimated_hrs }} hrs</div> -->
    </div>

    <div class="sla-container">
        <div class="sla_text">Sprint Stat</div>
        <div class="progress">
            <div class="progress-bar" role="progressbar" 
                :style="{ width: (new Date().getDate() / new Date(new Date().getFullYear(), new Date().getMonth() + 1, 0).getDate()) * 100 + '%' }">
            </div>
        </div>
        <div class="sla_text">{{ new Date().getDate() }} / {{ new Date(new Date().getFullYear(), new Date().getMonth() + 1, 0).getDate() }} days</div>
    </div>

    <div class="sprint_graph" style="position: relative; height: 40vh; width: 100%;">
        <canvas id="sprintChart" ref="sprintChartRef"></canvas>

    </div>
</template>


<style scoped>
.numbner_sla{
    width: 3rem;
    height: 1.5rem;
    border-radius: 0.25rem;
    border: 0;
    text-align: center;
    font-size: 0.7rem;
    margin-left: 0.5rem;
    margin-right: 0.5rem;
}
.numbner_sla:focus {
    outline: none;
    border-color: #27a295;
}
.progress {
    width: 40%;
    background-color: #ddd;
    border-radius: 0.25rem;
    height: 0.4rem;
    margin-left: 0.5rem;
    margin-right: 0.5rem;
}

.progress-bar {
    height: 100%;
    background-color: #27a295;
    border-radius: 0.25rem;
}

.sla_text {
    font-size: 0.7rem;
    margin-right: 0.5rem;
}

.sla-container {
    width: 20em;
    height: 3rem;
    border-radius: 0.5rem;
    background-color: #f5f5f5;
    margin-top: 1rem;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}
.sla-container:hover {
    background-color: #e0e0e0;
}

.sla-container:hover .progress-bar {
animation: progress 0.3s linear ;
}
@keyframes progress {
    0% {
        width: 0%;
    }
}

.sprint_graph {
    width: 20rem !important;
    height: 10rem !important;
    margin-top: 2rem !important;
    margin-bottom: 1rem !important;
}
</style>
