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
let esthours = ref(0);


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

function update_est() {
    console.log('Updating SLA...');
    console.log('Estimated Hours:', esthours.value); // Check the current value
    updateSLA();
}


// import " coockie from 'vue3-cookies";
import { useCookies } from 'vue3-cookies';
const { cookies } = useCookies();
const user= cookies.get('user');

watchEffect(() => {
    // Ensure data is available before drawing the chart
    if (!estimated_hrs.value) {
        estimated_hrs.value = 1;
        esthours.value = 1;
    } else {
        esthours.value = estimated_hrs.value;
    }

    if (loggs.value.length === 0) {
        loggs.value.push({
            user: user,
            logged: "0",
            date: new Date().toISOString()
        });
    }

    updateSLA();
});

onMounted(() => {
    console.log('Initial logged hours:', loggs.value);
    // updateSLA();
    // drawSprintChart();
    setTimeout(() => {
        drawSprintChart();
    },1000);
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

function add_log(event) {
    const newValue = parseInt(event.target.value, 10);
    const currentTotal = total_logged.value;

    if (newValue < currentTotal) {
        const difference = currentTotal - newValue;
        for (let i = loggs.value.length - 1; i >= 0 && difference > 0; i--) {
            const log = loggs.value[i];
            const loggedHours = parseInt(log.logged, 10);

            if (loggedHours <= difference) {
                difference -= loggedHours;
                loggs.value.splice(i, 1); 
            } else {
                log.logged = loggedHours - difference;
                break;
            }
        }
    } else {
        loggs.value.push({
            user: user,
            logged: newValue - currentTotal,
            date: new Date().toISOString()
        });
    }

    updateSLA();
    drawSprintChart();
}

const total_logged = computed(() => {
    return loggs.value.reduce((acc, log) => acc + parseInt(log.logged), 0);
});
</script>

<template>
    <div class="sla-container">
        <div class="sla_text">Time to SLA</div>
        <div class="progress">
            <div class="progress-bar" role="progressbar" :style="{ width: perscent_sla + '%' }">
            </div>
        </div>
        <div class="sla_text">
            <!-- {{ loggs.reduce((acc, log) => acc + parseInt(log.logged), 0) }} -->
              <input class="numbner_sla" type="number" @change="add_log($event)" min="0" :v-model="total_logged" :max="esthours" />
            /  <input class="numbner_sla" type="number" v-model="esthours" @input="update_est" /> hrs
        </div>
        <!-- <div class="sla_text">{{ total_logged }} / {{ estimated_hrs }} hrs</div> -->

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
    width: 2vw;
    padding: 0;
    margin: 0;
    height: 1.5vw;
    border-radius: 0.25vw;
    border: 0;
    text-align: center;
    font-size: 0.7vw;
    background-color: transparent;
}
.numbner_sla:hover {
    background-color: #f7f6f6;
}
.numbner_sla:focus {
    outline: none;
    border-color: #27a295;
}
.progress {
    width: 40%;
    background-color: #ddd;
    border-radius: 0.25vw;
    height: 0.4vw;
    margin-left: 0.5vw;
    margin-right: 0.5vw;
}

.progress-bar {
    height: 100%;
    background-color: #27a295;
    border-radius: 0.25vw;
}

.sla_text {
    font-size: 0.7vw;
    margin-right: 0.5vw;
}

.sla-container {
    width: 20vw;
    height: 3vw;
    border-radius: 0.5vw;
    background-color: #f5f5f5;
    margin-top: 1vw;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    transform: scale(0.9);
    padding: 0.4vw 0vw;
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
    width: 19vw !important;
    height: 8vw !important;
    margin-top:1.8vw !important;
    margin-bottom: 0.5vw !important;
    /* transform: scale(0.9); */
}
</style>
