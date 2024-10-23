<script setup>
import { ref, onMounted, watch, toRef, defineEmits } from 'vue';

const emit = defineEmits(); 

const get_employeees = document.baseMyURL + "/get_users"; 
const users = ref({}); 
const filtered_users = ref([]); 
const props = defineProps({
    cur_text: String,
    tot: {
        type: Boolean,
        default: true
    },
});

const cur_text_ref = toRef(props, 'cur_text');

onMounted(async () => {
    const response = await fetch(get_employeees);
    const data = await response.json();
    
    Object.keys(data).forEach((user, index) => {
        const user_info = user;
        users.value[index] = user_info.toLowerCase();
    });

    filtered_users.value = Object.values(users.value); 

    setInterval(() => {
        filter_users(); 
    }, 1000);
});


const panel = document.querySelector('.employee_list_con');
function filter_users() {
    filtered_users.value = Object.values(users.value).filter(user => user.includes(cur_text_ref.value.toLowerCase()));

}

watch(cur_text_ref, filter_users);

function highlightText(user) {
    if (!cur_text_ref.value) return user; 

    const regex = new RegExp(`(${cur_text_ref.value})`, 'gi');
    return user.replace(regex, '<span class="highlight">$1</span>');
}

function selectUser(user) {
    emit('select', user);
}
</script>

<template>
    <div class="employee_list_con">
        {{sty}}
        <div class="total_banner" v-if="tot">
            ({{ filtered_users.length }})</div>
        
        <div v-for="user in filtered_users" :key="user" class="employee_list">
            <span 
                v-html="highlightText(user)" 
                class="employee_name" 
                @click="selectUser(user)">
            </span>
        </div>
    </div>
</template>




<style scroped>
.total_banner{
    margin: 0.4vw 2vw;
    margin-top: 0.7vw;
    text-decoration: underline;
    text-align: right;
    background-color: transparent;
    position: fixed;
margin-left: 14.4vw;
}

.highlight {
    background-color: yellow; /* Change this to your preferred highlight color */
    font-weight: bold; /* Optional: make the highlighted text bold */
}



.employee_list_con{
    position: absolute;
    height: 15vw;
    width: 18vw;
    background: rgba(255, 255, 255, 1);
    border: 0.1vw solid #6f6f6f;  
    max-height: 15vw;
    height: auto;
    border-radius: 0.2vw;
    top: 19vw;
    left: 47vw;
    overflow: auto;
    overflow-x: hidden;
    cursor: pointer;
}

.employee_list_con::-webkit-scrollbar {
    width: 0.4vw;
}
.employee_list_con::-webkit-scrollbar-thumb {
    background-color: #6b6b6b;
    border-radius: 1vw;
}
.employee_list_con::-webkit-scrollbar-track {
    background-color: #f1f1f1;
}

.employee_list{
    padding: 0.6vw 1vw;
    font-size: 0.8vw;
    width: 100%;
}
.employee_name{
    padding: 0.6vw 1vw;
    font-size: 0.8vw;
    width: webkit-fill-available;
}
.employee_list:hover{
    background-color: rgb(216, 216, 216);
}

</style>