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

const get_tickets_url = document.baseMyURL + "/get";



let ticket_data = ref([{
    "chat_id": "tRAFcELKK5xiAK6FAAAD",
    "ticket_id": "SVC-000000",
    "user": "admin",
    "medium": "",
    "connection": "closed",
    "text": "wlpfo is declining transactions where the P025 field is set to 28, while transactions with P025 value 00 are being approved. The logs indicate an issue within the transaction processing logic related to the P025 field. Clarification is required for the correct values for P025.",
    "subject": "wlpfo Transaction Declined for P025 Value 28",
    "summary": "wlpfo is declining transactions where the P025 field is set to 28, while transactions with P025 value 00 are being approved. The logs indicate an issue within the transaction processing logic related to the P025 field. Clarification is required for the correct values for P025.",
    "attachments": [
        {
            "name": "Transaction Logs",
            "type": "text/plain",
            "url": "https://example.com/logs.txt",
            "details": "The logs show successful transactions when P025 is 00 and declined transactions when P025 is 28. Errors like \"[ERROR]: P025 invalid\" are present. The logs also contain details of GICC capture, GICC authorization request, compose message, and e-commerce transaction details. Further analysis suggests potential conflicts with specific transaction parameters or conditions related to P025 field validation.",
            "size": "4382"
        }
    ],
    "product_type": "wlpfo",
    "issue_type": "bug",
    "priority": "high",
    "story_points": "5",
    "estimation": "8",
    "analysis": "The issue likely stems from incorrect validation rules or logic for the P025 field within wlpfo. A code review and debugging of the transaction processing module, focusing on P025 handling, are recommended. Testing with various P025 values and different transaction scenarios will help isolate the problem. A potential workaround could involve temporarily disabling the specific P025 validation rule, if feasible, until a permanent fix is implemented.",
    "reply": "A ticket has been created to investigate the issue with wlpfo declining transactions for P025 value 28. We will analyze the provided logs and investigate the root cause of the problem. We'll keep you updated on the progress and provide a solution as soon as possible.",
    "assignee": "developer_1",
    "status": "closed",
    "created": "2021-07-15T10:00:00",
    "updated": "2021-07-15T10:00:00",
    "comments": [
        {
            "comment_id": "1",
            "user": "developer_1",
            "text": "I will start investigating the issue with P025 validation in wlpfo. I'll update you with my findings and progress.",
            "date": "2021-07-15T10:30:00"
        }
    ],
    "logged_hrs": [
        {
            "user": "developer_1",
            "logged": "2",
            "date": "2021-07-15T10:30:00"
        },
        {
            "user": "developer_1",
            "logged": "3",
            "date": "2021-07-16T10:30:00"
        }
    ]
},
{
    "chat_id": "tRAFcELKK5xiAK6FAAAD",
    "ticket_id": "SVC-11111",
    "user": "raj",
    "medium": "",
    "connection": "closed",
    "text": "wlpfo is declining transactions where the P025 field is set to 28, while transactions with P025 value 00 are being approved. The logs indicate an issue within the transaction processing logic related to the P025 field. Clarification is required for the correct values for P025.",
    "subject": "rajash wlpfo Transaction Declined for P025 Value 28",
    "summary": "wlpfo is declining transactions where the P025 field is set to 28, while transactions with P025 value 00 are being approved. The logs indicate an issue within the transaction processing logic related to the P025 field. Clarification is required for the correct values for P025.",
    "attachments": [
        {
            "name": "Transaction Logs",
            "type": "text/plain",
            "url": "https://example.com/logs.txt",
            "details": "The logs show successful transactions when P025 is 00 and declined transactions when P025 is 28. Errors like \"[ERROR]: P025 invalid\" are present. The logs also contain details of GICC capture, GICC authorization request, compose message, and e-commerce transaction details. Further analysis suggests potential conflicts with specific transaction parameters or conditions related to P025 field validation.",
            "size": "4382"
        }
    ],
    "product_type": "wlpfo",
    "issue_type": "bug",
    "priority": "high",
    "story_points": "5",
    "estimation": "8",
    "analysis": "The issue likely stems from incorrect validation rules or logic for the P025 field within wlpfo. A code review and debugging of the transaction processing module, focusing on P025 handling, are recommended. Testing with various P025 values and different transaction scenarios will help isolate the problem. A potential workaround could involve temporarily disabling the specific P025 validation rule, if feasible, until a permanent fix is implemented.",
    "reply": "A ticket has been created to investigate the issue with wlpfo declining transactions for P025 value 28. We will analyze the provided logs and investigate the root cause of the problem. We'll keep you updated on the progress and provide a solution as soon as possible.",
    "assignee": "admin",
    "status": "open",
    "created": "2021-07-15T10:00:00",
    "updated": "2021-07-15T10:00:00",
    "comments": [
        {
            "comment_id": "1",
            "user": "developer_1",
            "text": "I will start investigating the issue with P025 validation in wlpfo. I'll update you with my findings and progress.",
            "date": "2021-07-15T10:30:00"
        }
    ],
    "logged_hrs": [
        {
            "user": "developer_1",
            "logged": "2",
            "date": "2021-07-15T10:30:00"
        },
        {
            "user": "developer_1",
            "logged": "3",
            "date": "2021-07-16T10:30:00"
        }
    ]
},
{
    "chat_id": "tRAFcELKK5xiAK6FAAAD",
    "ticket_id": "SVC-11111",
    "user": "akil",
    "medium": "",
    "connection": "closed",
    "text": "wlpfo is declining transactions where the P025 field is set to 28, while transactions with P025 value 00 are being approved. The logs indicate an issue within the transaction processing logic related to the P025 field. Clarification is required for the correct values for P025.",
    "subject": "wlpfo Transaction Declined for P025 Value 28",
    "summary": "wlpfo is declining transactions where the P025 field is set to 28, while transactions with P025 value 00 are being approved. The logs indicate an issue within the transaction processing logic related to the P025 field. Clarification is required for the correct values for P025.",
    "attachments": [
        {
            "name": "Transaction Logs",
            "type": "text/plain",
            "url": "https://example.com/logs.txt",
            "details": "The logs show successful transactions when P025 is 00 and declined transactions when P025 is 28. Errors like \"[ERROR]: P025 invalid\" are present. The logs also contain details of GICC capture, GICC authorization request, compose message, and e-commerce transaction details. Further analysis suggests potential conflicts with specific transaction parameters or conditions related to P025 field validation.",
            "size": "4382"
        }
    ],
    "product_type": "wlpfo",
    "issue_type": "bug",
    "priority": "high",
    "story_points": "5",
    "estimation": "8",
    "analysis": "The issue likely stems from incorrect validation rules or logic for the P025 field within wlpfo. A code review and debugging of the transaction processing module, focusing on P025 handling, are recommended. Testing with various P025 values and different transaction scenarios will help isolate the problem. A potential workaround could involve temporarily disabling the specific P025 validation rule, if feasible, until a permanent fix is implemented.",
    "reply": "A ticket has been created to investigate the issue with wlpfo declining transactions for P025 value 28. We will analyze the provided logs and investigate the root cause of the problem. We'll keep you updated on the progress and provide a solution as soon as possible.",
    "assignee": "developer_1",
    "status": "open",
    "created": "2021-07-15T10:00:00",
    "updated": "2021-07-15T10:00:00",
    "comments": [
        {
            "comment_id": "1",
            "user": "developer_1",
            "text": "I will start investigating the issue with P025 validation in wlpfo. I'll update you with my findings and progress.",
            "date": "2021-07-15T10:30:00"
        }
    ],
    "logged_hrs": [
        {
            "user": "developer_1",
            "logged": "2",
            "date": "2021-07-15T10:30:00"
        },
        {
            "user": "developer_1",
            "logged": "3",
            "date": "2021-07-16T10:30:00"
        }
    ]
}
]);

onMounted(() => {

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

    loading.value = false;
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
                    <div v-for="(mail, index) in mail_json" :key="index" class="cat_section" @click="open_ticket(mail.ticket_id)">
                        <div class="cat_section_bar">
                            {{ index }}
                            <div class="from_">{{ mail.from }}</div>
                            <div class="subjj_">{{ mail.subject }}</div>
                            <div :style="{ color: mail.status === 'open' ? 'green' : 'red' }"> {{ mail.status }}</div>
                            
                            <div>{{ new Date(mail.updated).toLocaleString() }}</div>
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
}
.subjj_{
    max-width: 35vw;
    min-width: 35vw;
}
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