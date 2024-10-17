<script setup>
import BreadCrumb from '@/components/BreadCrumb.vue';
import NavigationBarView2 from '@/views/NavigationBarView_2.vue';
import { onMounted, ref } from 'vue';
import SidePane from '@/components/SidePane.vue';
import LoaderToast from '@/components/LoaderToast.vue';
import { faLeaf } from '@fortawesome/free-solid-svg-icons';

import { useCookies } from 'vue3-cookies';

let bread_path_json = {
    "NULLBYTE": "/",
    "TICKETS": "/tickets",
    "LIST TICKETS": "/list_tickets"
};

const loading = ref(true);

const get_tickets_url = "http://localhost:5000/get_tickets";

// get category passed via url params


const ticket_data = ref([]);  

onMounted(async () => {
    loading.value = true;
    console.log('mounted');

    try {
        const response = await fetch(get_tickets_url);
        const data = await response.json();
        Object.keys(data).forEach(ticket_id => {
            const ticket_info = data[ticket_id];
            const tmp_tick = ticket_info.closed_chat || ticket_info;
            ticket_data.value.push(tmp_tick);
        });

        console.log("jesvi : ", ticket_data.value);

    } catch (error) {
        console.error('Error fetching tickets:', error);
    } finally {
        loading.value = false;
    }
});

function open_ticket(ticket_id) {
    // open in new tab
    window.open(`/ticket/${ticket_id}`, '_blank');
}

const { cookies } = useCookies();
const current_user = cookies.get('user');

if (!current_user) {
    console.log('cookie not found');
    alert('Please login again to continue, could not find user details');
}

function category_sel(category, event) {
    let cat_section_bar = document.getElementById('cat_section_bar');
    Array.from(cat_section_bar.childNodes).forEach((child) => {
        if (child.classList) {
            child.classList.remove('cat_act');
        }
    });
    event.target.classList.add('cat_act');

    let ticket_list_data = document.getElementById('ticket_list_data');
    let ticket_list = ticket_list_data.getElementsByTagName('tr');
    for (let i = 0; i < ticket_list.length; i++) {
        let ticket = ticket_list[i];
        let status = ticket.getElementsByTagName('td')[9].innerText;
        if (category === 'all') {
            ticket.style.display = 'table-row';

        } else if (category === 'open' && status === 'open') {
            ticket.style.display = 'table-row';
        } else if (category === 'closed' && status === 'closed') {
            ticket.style.display = 'table-row';
        } else if (category === 'pending' && status === 'pending') {
            ticket.style.display = 'table-row';
        }
        // else if (category === 'action' && status === 'action') {
        // ticket.style.display = 'table-row';} 
        else if (category === 'my_tickets' && (ticket.getElementsByTagName('td')[6].innerText.toLowerCase() === current_user || ticket.getElementsByTagName('td')[7].innerText.toLowerCase() === current_user)) {
            ticket.style.display = 'table-row';
        }

        else {
            ticket.style.display = 'none';
        }
    }
}


function search_results() {
    let search = document.getElementById('search').value.toLowerCase();
    let ticket_list_data = document.getElementById('ticket_list_data');
    let ticket_list = ticket_list_data.getElementsByTagName('tr');
    for (let i = 0; i < ticket_list.length; i++) {
        let ticket = ticket_list[i];
        let fields = Array.from(ticket.getElementsByTagName('td')).map(td => td.innerText.toLowerCase());
        let match = fields.some(field => field.includes(search));
        if (match) {
            ticket.style.display = 'table-row';
            fields.forEach((field, index) => {
                let regex = new RegExp(`(${search})`, 'gi');
                ticket.getElementsByTagName('td')[index].innerHTML = field.replace(regex, '<span style="background-color: yellow;">$1</span>');
            });
        } else {
            ticket.style.display = 'none';
        }
    }
}
function getPriorityColor(priority) {
    if (priority === 'high') {
        return 'red';
    } else if (priority === 'medium') {
        return 'orange';
    } else if (priority === 'low') {
        return 'green';
    } else {
        return 'black';
    }
}
function getStoryPointsColor(story_points) {
    if (story_points === '5') {
        return 'maroon';
    } else if (story_points === '3') {
        return 'orange';
    } else if (story_points === '1') {
        return 'green';
    } else {
        return 'black';
    }
}


</script>


<template>
    <LoaderToast :loading="loading" />
    <!-- <NavigationBarView /> -->
    <NavigationBarView2 />
    <div class="home-container">
        <SidePane />
        <div class="main-pane">
            <BreadCrumb :data="bread_path_json" />
            <div class="tile-container">
                <h1 class="main_title">Tickets View<div class="ticket_id">{{ ticket_data.ticket_id }}</div>
                </h1>
                <div class="cat_section_bar cat_on">
                    <div class="cat_section_bar " id="cat_section_bar">
                        <div class="cat_section cat_act" @click="category_sel('all', $event)">All ({{ ticket_data.length
                            }})</div>
                        <div class="cat_section" @click="category_sel('open', $event)" id="open">Open ({{
                            ticket_data.filter(ticket => ticket.status == 'open').length }})</div>
                        <div class="cat_section" @click="category_sel('closed', $event)" id="closed">Closed ({{
                            ticket_data.filter(ticket => ticket.status == 'closed').length }})</div>
                        <div class="cat_section" @click="category_sel('pending', $event)" id="pending">Pending ({{
                            ticket_data.filter(ticket => ticket.status == 'waiting for information').length }})</div>
                        <!-- <div class="cat_section" @click="category_sel('action', $event)">Action ({{ ticket_data.filter(ticket => ticket.status === 'action').length }})</div> -->
                        <div class="cat_section" @click="category_sel('my_tickets', $event)" id="my_tickets">My Tickets ({{
                            ticket_data.filter(ticket => ticket.user.toLowerCase() === current_user ||
                            ticket.assignee.toLowerCase() === current_user).length }})</div>
                    </div>
                    <div class="cat_search">
                        <input type="text" placeholder="Search" class="top_search" id="search"
                            @keyup="search_results" />
                        <div class="cat_section_bar">
                            <button class="btnsort"><img src="https://img.icons8.com/ios/50/000000/filter.png" />
                            </button>
                        </div>
                    </div>

                </div>
                <div class="ticket_list">
                    <table class="table_skirt">
                        <thead>
                            <tr>
                                <th>S.No</th>
                                <th>Ticket ID</th>
                                <th>Subject</th>
                                <th>Priority</th>
                                <th>Story Points</th>
                                <th>Product</th>
                                <th>Created By</th>
                                <th>Assignee</th>
                                <th>SLA</th>
                                <th>Status</th>
                                <th>Created</th>
                                <th>Updated</th>
                            </tr>
                        </thead>
                        <tbody id="ticket_list_data">
                            <tr v-for="(ticket, index) in ticket_data" :key="ticket.ticket_id"
                                @click="open_ticket(ticket.ticket_id)">
                                <td>{{ index + 1 }}</td>
                                <td>{{ ticket.ticket_id }}</td>
                                <td><a>{{ ticket.subject }}</a></td>
                                <td :style="{ color: getPriorityColor(ticket.priority) }">{{ ticket.priority }}</td>
                                <td :style="{ color: getStoryPointsColor(ticket.story_points) }">{{ ticket.story_points
                                    }}</td>
                                <td>{{ ticket.product_type }}</td>
                                <td
                                    :style="{ fontStyle: ticket.user === current_user ? '' : 'none', color: ticket.user === current_user ? 'teal' : 'inherit' }">
                                    {{ ticket.user }}</td>
                                <td
                                    :style="{ fontStyle: ticket.assignee === current_user ? '' : 'none', color: ticket.assignee === current_user ? 'teal' : 'inherit' }">
                                    {{ ticket.assignee }}</td>
                                <td>{{ ticket.logged_hrs ? ticket.logged_hrs.reduce((total, log) => total + parseFloat(log.logged), 0) : 0 }}/{{ ticket.estimation }} hrs</td>
                                <td
                                    :style="{ color: ticket.status && ticket.status.toLocaleLowerCase() === 'open' ? 'green' : ticket.status && ticket.status.toLocaleLowerCase() === 'closed' ? 'red' : ticket.status && ticket.status.toLocaleLowerCase() === 'pending' ? 'orange' : ticket.status && ticket.status.toLocaleLowerCase() === 'waiting for information' ? 'blue' : 'black' }">
                                    {{ ticket.status }}</td>
                                <td>{{ ticket.created }}</td>
                                <td>{{ ticket.updated }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

        </div>

    </div>
</template>

<style scoped>
.cat_search {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: space-between;
    align-items: center;
    gap: 1vw;
}

.btnsort {
    background-color: #46BEAA;
    color: white;

    padding: 0.7vw 0vw;
    border: none;
    border-radius: 0.3vw;
    cursor: pointer;
    text-align: center;
    border: 0.1vw solid #46BEAA;
    margin: auto;
    height: 2.5vw;
    width: 3vw;
}

.btnsort:hover {
    background-color: white;
    border: 0.1vw solid #46BEAA;
}

.btnsort:hover img {
    filter: invert(0);
}

.btnsort img {
    width: 1.2vw;
    height: 1.1vw;
    filter: invert(1);
}

.first_line {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: space-between;
    align-items: baseline;
    width: 100%;
}

.creat_form_cont {
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: center;
    align-items: stretch;
    /* width: 63%; */
    width: 78%;
    margin: 0vw 5vw;
    /* gap: 1vw; */
}

textarea {
    transition: none;
}

input,
textarea,
select {
    width: 20vw;
    height: 1.5vw;
    min-height: 1.5vw;
    border: 0.1vw solid #81818175;
    border-radius: 0.3vw;
    padding: 0.5vw;
    margin-top: 0.5vw;
    font: 1vw 'wl1';
    color: black;
}

input:focus,
textarea:focus,
select:focus {
    outline: none;
    border: 0.1vw solid #46BEAA;
}

/* input, textarea, select{   placeholder: font size */
::placeholder {
    font: 0.9vw 'wl1';
    color: #81818175;
}

select {
    height: initial;
    width: 21vw;
}

.input_cont_2 {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: space-between;
    align-items: baseline;
    width: 100%;
    margin-top: 0.5vw;
}

.desc {
    height: 7vw;
    width: 100%;
}

.input_field {}

.input_cont {
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: center;
    align-items: baseline;
    color: grey;
    margin-top: 1vw;
}

.tile-container {
    /* margin-top: 2vw; */
    /* width: 80%; */
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    align-items: center;
    /* justify-content: flex-start; */
    /* gap: 1vw; */
    /* margin-top: 1vw; */
    margin: 2vw 1vw;
    width: 70vw;
    /* width: 63vw; */
    /* margin-bottom: 7vw; */
    height: -webkit-fill-available;

}

.main_title {
    font-family: 'wl2';
    font-size: 2vw;
    font-weight: 900;
    /* width: 90%; */
    display: flex;
    flex-direction: row;
    gap: 1vw;
    align-content: center;
    align-items: baseline;
    justify-content: flex-start;
    flex-wrap: nowrap;
    width: 90%;
    margin-bottom: 2vw;
}

.ticket_id {
    font-size: 0.8vw;
    font-weight: 100;
    color: rgb(197, 197, 197);
}

.main-pane {
    display: flex;
    align-items: flex-start;
    flex-direction: column;
    width: 100%;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: space-between;
    height: max-content;
    overflow-y: scroll;
    overflow-x: hidden;
    height: 90vh;
}

.main-pane * {
    /* color: CADETBLUE; */
    color: rgb(72, 72, 72);
}

.home-container {
    justify-content: flex-start;
    display: flex;
    flex-direction: row;
    overflow: hidden;
    height: fill-available;
    height: 90vh;


}

.btn {
    background-color: #46BEAA;
    color: white;
    padding: 0.5vw 3vw;
    /* min-width: 14vw; */
    /* max-width: 14vw; */
    border: none;
    border-radius: 0.3vw;
    cursor: pointer;
    text-align: center;
    border: 0.1vw solid #46BEAA;
    /* margin: auto; */
}

.btn:hover {
    background-color: white;
    color: #46BEAA;
    border: 0.1vw solid #46BEAA;
}

.btn_cancel {
    background-color: white;
    color: #46BEAA;
    /* padding: 0.5vw 0vw; */
    min-width: 5vw;
    /* max-width: 14vw; */
    border: none;
    border-radius: 0.3vw;
    cursor: pointer;
    text-align: center;

    /* margin: auto; */
    /* margin-top: 3vw; */
    /* margin-bottom: 3vw; */
    display: flex;
    justify-content: center;
    align-items: center;
    /* margin: auto; */
    padding: 0.5vw 0.5vw;
    border: 0.1vw solid #000000;
    background-color: grey;
    filter: invert(1);
}

.btn_cancel:hover {
    border: 0.1vw solid #be4646;
    background-color: #000000;

}

.btn_cancel:hover img {
    filter: invert(1);
}

.btn_cancel img {
    width: 1.5vw;
    height: 1.5vw;
}

.but_con {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: flex-start;
    justify-content: flex-start;
    align-items: flex-start;
    gap: 1vw;
    /* margin-top: 3vw;
    margin-bottom: 3vw; */
    width: auto;
    margin-top: 3.5vw;
}


.attach_cont {
    display: flex;
    flex-direction: row;
    align-items: flex-end;
    align-content: center;
    flex-wrap: nowrap;
    justify-content: space-between;
}

.attach_cont_files {
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    align-items: flex-start;
    justify-content: center;
}

.ai_button {
    height: 2.5vw;
    filter: invert(1);
    padding: 0vw 2vw;
    color: black;
    /* padding: 0 0; */
    /* padding: 0vw 1vw; */
    background-color: #bb8484;
    min-width: 0;
    display: flex;
    gap: 1vw;
}

.ai_button:hover {
    background: #000000;
    color: white;
}

.attachment-item {
    display: flex;
    align-items: center;
    margin-top: 0.5vw;
    flex-direction: row-reverse;
    flex-wrap: nowrap;
    width: 20vw;
    gap: 2vw;
    justify-content: flex-end;
}

.attachment-item:hover {
    background-color: #f0f0f0;
    cursor: pointer;
}

.attachments-list {
    margin-top: 1vw;
    font-size: 0.8vw;
}

.btn_cancel_file {
    padding: 0vw 0.3vw;
    color: rgba(77, 4, 4, 0.557);
    background-color: white;
    border: 0.05vw solid rgb(77, 4, 4);
    border-radius: 0.3vw;
    cursor: pointer;
}

.btn_cancel_file:hover {
    background-color: rgb(208, 44, 44);
    color: white;
}

.btn_cancel_file::after {
    content: 'X';
}

._attch_but {
    background-color: grey;
    border-color: white;
    margin-top: 0.6vw;
}

._attch_but:hover {
    background-color: rgb(65, 65, 65);
    border-color: white;
    color: white;
}

.f_size {
    display: flex;
    align-items: center;
    gap: 0.5vw;
}

.f_size_con {
    display: flex;
    width: -webkit-fill-available;
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: space-between;
    justify-content: space-between;
    align-items: center;
}

.cat_section {
    padding: 0.5vw 1vw;
    /* border-radius: 0.3vw; */
    /* background-color: #6a6a6a2d; */
    border-bottom: 0.1vw solid #6a6a6a2d;
    color: rgb(85, 85, 85);
    cursor: pointer;
    font-size: 0.9vw;
}

.cat_section_bar {
    display: flex;
    gap: 1vw;
    height: 2.5vw;
}

.cat_section:hover {
    background-color: #6a6a6a2d;
}

.cat_on {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: space-around;
    justify-content: space-between;
    align-items: stretch;
    width: 90%;
}

.cat_act {
    border-bottom: 0.1vw solid #000000;
    background-color: rgba(0, 0, 0, 0.03);
    min-width: max-content;
}

.top_search {
    border: none;
    border-radius: 0vw;
    border-bottom: 0.1vw solid #6a6a6a2d;
    padding: 0.2vw;
    width: 14vw;
}

.top_search:focus {
    border: none;
    border-bottom: 0.1vw solid #46BEAA;
}

.ticket_list {
    margin-top: 1vw;
    width: 100%;
    overflow: auto;
    font-size: 0.8vw;
    width: 92%;
    height: -webkit-fill-available;
}

.ticket_list::-webkit-scrollbar {
    width: 0.4vw;
    height: 0.3vw;
}

.ticket_list::-webkit-scrollbar-thumb {
    background-color: #bbbbbb;
    border-radius: 0.3vw;
}

.ticket_list::-webkit-scrollbar-track {
    background-color: #f1f1f1;
}

.table {
    width: 100%;
    background-color: white;
    color: #333;
    /* Dark grey for table text */
}

thead {
    background-color: #959595;
    /* Light grey for thead background */
}

thead th {
    color: #ffffff !important;
    /* Dark grey for thead text */

}

tbody tr {
    width: max-content;
    background-color: #ffffff;
    /* White background for table rows */
    cursor: pointer;
}

tbody tr:nth-child(odd) {
    background-color: #f5f5f5;
    /* Light grey for alternate rows */
}

tbody tr:hover {
    background-color: #e0e0e0;
    /* Darker grey on hover */
}

td,
th {
    padding: 0.75vw;
    /* border-bottom: 1px solid #ccc; */
}

.table_skirt {
    width: max-content;
}

td a {
    text-decoration: underline;
    color: blue !important;
    font-family: wl1;
}

td a:hover {
    color: #46BEAA !important;
}
</style>