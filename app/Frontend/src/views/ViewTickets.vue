<script setup>
import BreadCrumb from '@/components/BreadCrumb.vue';
import NavigationBarView2 from '@/views/NavigationBarView_2.vue';
import { onMounted, ref } from 'vue';
import SidePane from '@/components/SidePane.vue';
import LoaderToast from '@/components/LoaderToast.vue';
import { faLeaf } from '@fortawesome/free-solid-svg-icons';

let bread_path_json = {
    "NULLBYTE": "/",
    "TICKETS": "/tickets",
    "LIST TICKETS": "/list_tickets"
};

const loading = ref(true);

const get_tickets_url = "http://localhost:5000/get_tickets";


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
    "assingee": "developer_1",
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
    "assingee": "developer_1",
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
    "assingee": "developer_1",
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
    loading.value = false;
});

function open_ticket(ticket_id) {
    console.log(ticket_id);
    // this.$router.push('/ticket/' + ticket_id);
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
                    <div class="cat_section_bar ">
                        <div class="cat_section cat_act">All</div>
                        <div class="cat_section">Open</div>
                        <div class="cat_section">Closed</div>
                        <div class="cat_section">Pending</div>
                        <div class="cat_section">Action</div>
                    </div>
                    <div class="cat_search">
                        <input type="text" placeholder="Search" class="top_search" />
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
                        <tbody>
                            <tr v-for="(ticket, index) in ticket_data" :key="ticket.ticket_id">
                                <td>{{ index + 1 }}</td>
                                <td>{{ ticket.ticket_id }}</td>
                                <td>{{ ticket.subject }}</td>
                                <td>{{ ticket.priority }}</td>
                                <td>{{ ticket.story_points }}</td>
                                <td>{{ ticket.product_type }}</td>
                                <td>{{ ticket.user }}</td>
                                <td>{{ ticket.assignee }}</td>
                                <td>{{ ticket.estimation }} hrs</td>
                                <td>{{ ticket.status }}</td>
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
    gap: 1rem;
}

.btnsort {
    background-color: #46BEAA;
    color: white;

    padding: 0.7rem 0rem;
    border: none;
    border-radius: 0.3rem;
    cursor: pointer;
    text-align: center;
    border: 0.1rem solid #46BEAA;
    margin: auto;
    height: 2.5rem;
    width: 3rem;
}

.btnsort:hover {
    background-color: white;
    border: 0.1rem solid #46BEAA;
}

.btnsort:hover img {
    filter: invert(0);
}

.btnsort img {
    width: 1.2rem;
    height: 1.1rem;
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
    margin: 0rem 5rem;
    /* gap: 1rem; */
}

textarea {
    transition: none;
}

input,
textarea,
select {
    width: 20rem;
    height: 1.5rem;
    min-height: 1.5rem;
    border: 0.1rem solid #81818175;
    border-radius: 0.3rem;
    padding: 0.5rem;
    margin-top: 0.5rem;
    font: 1rem 'wl1';
    color: black;
}

input:focus,
textarea:focus,
select:focus {
    outline: none;
    border: 0.1rem solid #46BEAA;
}

/* input, textarea, select{   placeholder: font size */
::placeholder {
    font: 0.9rem 'wl1';
    color: #81818175;
}

select {
    height: initial;
    width: 21rem;
}

.input_cont_2 {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: space-between;
    align-items: baseline;
    width: 100%;
    margin-top: 0.5rem;
}

.desc {
    height: 7rem;
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
    margin-top: 1rem;
}

.tile-container {
    /* margin-top: 2rem; */
    /* width: 80%; */
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    align-items: center;
    /* justify-content: flex-start; */
    /* gap: 1rem; */
    /* margin-top: 1rem; */
    margin: 2rem 1rem;
    width: 70vw;
    /* width: 63vw; */
    /* margin-bottom: 7rem; */
    height: -webkit-fill-available;

}

.main_title {
    font-family: 'wl2';
    font-size: 2rem;
    font-weight: 900;
    /* width: 90%; */
    display: flex;
    flex-direction: row;
    gap: 1rem;
    align-content: center;
    align-items: baseline;
    justify-content: flex-start;
    flex-wrap: nowrap;
    width: 90%;
    margin-bottom: 2rem;
}

.ticket_id {
    font-size: 0.8rem;
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
    padding: 0.5rem 3rem;
    /* min-width: 14rem; */
    /* max-width: 14rem; */
    border: none;
    border-radius: 0.3rem;
    cursor: pointer;
    text-align: center;
    border: 0.1rem solid #46BEAA;
    /* margin: auto; */
}

.btn:hover {
    background-color: white;
    color: #46BEAA;
    border: 0.1rem solid #46BEAA;
}

.btn_cancel {
    background-color: white;
    color: #46BEAA;
    /* padding: 0.5rem 0rem; */
    min-width: 5rem;
    /* max-width: 14rem; */
    border: none;
    border-radius: 0.3rem;
    cursor: pointer;
    text-align: center;

    /* margin: auto; */
    /* margin-top: 3rem; */
    /* margin-bottom: 3rem; */
    display: flex;
    justify-content: center;
    align-items: center;
    /* margin: auto; */
    padding: 0.5rem 0.5rem;
    border: 0.1rem solid #000000;
    background-color: grey;
    filter: invert(1);
}

.btn_cancel:hover {
    border: 0.1rem solid #be4646;
    background-color: #000000;

}

.btn_cancel:hover img {
    filter: invert(1);
}

.btn_cancel img {
    width: 1.5rem;
    height: 1.5rem;
}

.but_con {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: flex-start;
    justify-content: flex-start;
    align-items: flex-start;
    gap: 1rem;
    /* margin-top: 3rem;
    margin-bottom: 3rem; */
    width: auto;
    margin-top: 3.5rem;
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
    height: 2.5rem;
    filter: invert(1);
    padding: 0rem 2rem;
    color: black;
    /* padding: 0 0; */
    /* padding: 0rem 1rem; */
    background-color: #bb8484;
    min-width: 0;
    display: flex;
    gap: 1rem;
}

.ai_button:hover {
    background: #000000;
    color: white;
}

.attachment-item {
    display: flex;
    align-items: center;
    margin-top: 0.5rem;
    flex-direction: row-reverse;
    flex-wrap: nowrap;
    width: 20rem;
    gap: 2rem;
    justify-content: flex-end;
}

.attachment-item:hover {
    background-color: #f0f0f0;
    cursor: pointer;
}

.attachments-list {
    margin-top: 1rem;
    font-size: 0.8rem;
}

.btn_cancel_file {
    padding: 0rem 0.3rem;
    color: rgba(77, 4, 4, 0.557);
    background-color: white;
    border: 0.05rem solid rgb(77, 4, 4);
    border-radius: 0.3rem;
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
    margin-top: 0.6rem;
}

._attch_but:hover {
    background-color: rgb(65, 65, 65);
    border-color: white;
    color: white;
}

.f_size {
    display: flex;
    align-items: center;
    gap: 0.5rem;
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
    padding: 0.5rem 1rem;
    /* border-radius: 0.3rem; */
    /* background-color: #6a6a6a2d; */
    border-bottom: 0.1rem solid #6a6a6a2d;
    color: rgb(85, 85, 85);
    cursor: pointer;
    font-size: 0.9rem;
}

.cat_section_bar {
    display: flex;
    gap: 1rem;
    height: 2.5rem;
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
.cat_act{
    border-bottom: 0.1rem solid #000000;
}
.top_search {
    border: none;
    border-radius: 0rem;
    border-bottom: 0.1rem solid #6a6a6a2d;
    padding: 0.2rem;
    width: 14rem;
}

.top_search:focus {
    border: none;
    border-bottom: 0.1rem solid #46BEAA;
}

.ticket_list {
    margin-top: 1rem;
    width: 100%;
    overflow: auto;
    font-size: 0.8rem;
    width: 92%;
    height: -webkit-fill-available;
}
.ticket_list::-webkit-scrollbar {
    width: 0.4rem;
    height: 0.3rem;
}
.ticket_list::-webkit-scrollbar-thumb {
    background-color: #bbbbbb;
    border-radius: 0.3rem;
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
    padding: 0.75rem;
    /* border-bottom: 1px solid #ccc; */
}

.table_skirt {
    width: max-content;
}
</style>