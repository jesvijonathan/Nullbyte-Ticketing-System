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
    "INBOX": "/inbox",
};

const loading = ref(true);

const get_tickets_url = document.baseMyURL + "/get_tickets";


let ticket_data = ref([
]);





let get_tickets = document.baseMyURL+"/get_tickets";

onMounted(async () => {

    loading.value = true;
    console.log('mounted');

    // fetch(get_tickets_url)
    //     .then(response => response.json())
    //     .then(data => {
    //         console.log(data);
    //         ticket_data.value = data;
    //     });

    console.log(ticket_data.value);
    let category = window.location.search.split('=')[1];

    const response = await fetch(get_tickets);
        const data = await response.json();
        // console.log("jesvi ::::", data)
        Object.keys(data).forEach(ticket_id => {
            console.log("jesvi ::::", data[ticket_id])
            // if (data[ticket_id].medium == 'chat') {
            const ticket_info = data[ticket_id];
            const tmp_tick = ticket_info.closed_chat || ticket_info;
            console.log("jesvi ::::", tmp_tick)
            ticket_data.value.push(tmp_tick);
            // }
        });

      console.log("#####jesvi :", ticket_data.value)

    loading.value = false;
});

function open_ticket(ticket_id) {
    // open in new tab
    window.open(`/ticket/${ticket_id}`, '_blank');
}

const { cookies } = useCookies();
const current_user = cookies.get('user');



// {
//     "analysis": "The performance issue could stem from various factors introduced by the latest installation, such as database changes, new features, or configuration modifications.  Analyzing logs and performance metrics will be crucial to identifying the bottleneck.",
//     "assignee": "unassigned",
//     "attachments": [],
//     "channel": "closed",
//     "chat_id": "j43BQYyGMTLiOJybAAAN",
//     "comments": [],
//     "created": "2024-10-23T06:26:47",
//     "estimation": 0,
//     "issue_type": "bug",
//     "last_modified": "2024-10-23T06:26:47",
//     "medium": "chat",
//     "priority": "medium",
//     "product_type": "wlpfo",
//     "reopens": 0,
//     "resolution": null,
//     "score": 0,
//     "status": "open",
//     "story_points": 3,
//     "subject": "WLPFO Performance Degradation After Latest Installation",
//     "summary": "WLPFO performance has degraded after the latest installation, impacting user experience.  Additional information is needed to identify the root cause and implement a solution.",
//     "team": null,
//     "text": "The user reported a significant slowdown in WLPFO performance following the recent installation.  Further details are required to pinpoint the affected tasks and quantify the performance decrease.",
//     "ticket_id": "7",
//     "type": null,
//     "user": "unassigned",
//     "worklogs": []
// }


if (!current_user) {
    console.log('cookie not found');
    alert('Please login again to continue, could not find user details');
}

let mail_json = ref({
    "1" : {
        "from": "admin",
        "subject": "wlpfo Transaction Declined for P025 Value 28",
        "date": "2021-07-15T10:00:00",
        "updated": "2021-07-15T10:00:00",
        "status": "open",
        "action": "",
        "priority" : "low",
        "ticket_id": "SVC-000000",
        "text": "wlpfo is declining transactions where the P025 field is set to 28, while transactions with P025 value 00 are being approved. The logs indicate an issue within the transaction processing logic related to the P025 field. Clarification is required for the correct values for P025.",
        "attachments": [
            {
                "name": "Transaction Logs",
                "type": "text/plain",
                "url": "https://example.com/logs.txt",
                "details": "The logs show successful transactions when P025 is 00 and declined transactions when P025 is 28. Errors like \"[ERROR]: P025 invalid\" are present. The logs also contain details of GICC capture, GICC authorization request, compose message, and e-commerce transaction details. Further analysis suggests potential conflicts with specific transaction parameters or conditions related to P025 field validation.",
                "size": "4382"
            }
        ]
    },
    "2" : {
        "from": "raj",
        "subject": "rajash wlpfo Transaction Declined for P025 Value 28",
        "date": "2021-07-15T10:00:00",
        "updated" : "2021-07-15T10:00:00",
        "status": "open",
        "priority" : "high",
        "action": "admin", 
        "ticket_id": "SVC-11111",
        "text": "wlpfo is declining transactions where the P025 field is set to 28, while transactions with P025 value 00 are being approved. The logs indicate an issue within the transaction processing logic related to the P025 field. Clarification is required for the correct values for P025.",
        "attachments": [
            {
                "name": "Transaction Logs",
                "type": "text/plain",
                "url": "https://example.com/logs.txt",
                "details": "The logs show successful transactions when P025 is 00 and declined transactions when P025 is 28. Errors like \"[ERROR]: P025 invalid\" are present. The logs also contain details of GICC capture, GICC authorization request, compose message, and e-commerce transaction details. Further analysis suggests potential conflicts with specific transaction parameters or conditions related to P025 field validation.",
                "size": "4382"
            }
        ]
    }
})



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
                <h1 class="main_title">Mail Inbox<div class="ticket_id">{{ ticket_data.ticket_id }}</div>
                </h1>

                <div class="ticket_list">
                    <div v-for="(mail, index) in ticket_data" :key="index" class="cat_section" @click="open_ticket(mail.ticket_id)" >
                        <div class="cat_section_bar">
                            {{ index }}
                            <div class="from_">{{ mail.user }}</div>
                            <div class="subjj_">{{ mail.subject }}</div>
                            <div :style="{ color: mail.status === 'open' ? 'green' : 'red' }"> {{ mail.status }}</div>
                            
                            <div>{{ new Date(mail.created).toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true }).replace(',', '').replace(' ', ' ') }}</div>
                            <div v-if="mail.action && mail.action === current_user" class="btnsort_" @click="open_ticket(mail.ticket_id)">
                                Approve
                            </div>
                            <div v-else class="btnsort_" @click="open_ticket(mail.ticket_id)">
                                View
                            </div>
                        </div>
                        </div>
                </div>
            </div>

        </div>

    </div>
</template>

<style scoped>
.btnsort_{
    background-color: #46BEAA;
    color: white;
    border: none;
    border-radius: 0.3vw;
    cursor: pointer;
    text-align: center;
    /* border: 0.1vw solid #46BEAA; */
    min-width: 4vw;
    font-size: 0.8vw;
    padding: 0.3vw;
    color: white !important;
}
.btnsort_:hover{
    
    background-color: #2a7a6d;
}
.from_{
    max-width: 4vw;
    min-width: 4vw;
    overflow: hidden;   
}
.subjj_{
    max-width: 35vw;
    min-width: 35vw;
    
    overflow: hidden;   
}
.cat_search {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: space-between;
    align-items: center;
    gap: 1vw;
    
    overflow: hidden;   
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
    align-content: space-between;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: space-between;
    align-items: center;
}

.cat_section:hover {
    background-color: #6a6a6a2d;
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


</style>