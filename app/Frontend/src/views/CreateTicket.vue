<script setup>
import BreadCrumb from '@/components/BreadCrumb.vue';
import NavigationBarView2 from '@/views/NavigationBarView_2.vue';
import { onMounted, ref } from 'vue';
import SidePane from '@/components/SidePane.vue';
import LoaderToast from '@/components/LoaderToast.vue';
import { faLeaf } from '@fortawesome/free-solid-svg-icons';

import { useRouter } from 'vue-router';

const router = useRouter();

let bread_path_json = {
    "NULLBYTE": "/",
    "TICKETS": "/tickets",
    "CREATE TICKET": "/create_ticket",
};

const attachments = ref([]);

const handleFileChange = (event) => {
    loading.value = true;
    const files = Array.from(event.target.files);
    files.forEach(file => {
        const reader = new FileReader();
        reader.onload = (e) => {
            attachments.value.push({
                name: file.name,
                type: file.type,
                size: file.size,
                data: btoa(e.target.result)
            });
        };
        reader.readAsDataURL(file); // or reader.readAsArrayBuffer(file) if needed
    });
    event.target.value = '';
    loading.value = false;
};


const removeAttachment = (index) => {
    attachments.value.splice(index, 1);
};


const loading = ref(true);

const get_ticket_url = "http://localhost:5000/get_ticket";
const get_incomplete_ticket_url = "http://localhost:5000/get_incomplete_ticket";

import { useCookies } from 'vue3-cookies';

const current_user = ref(null);
const { cookies } = useCookies();

if (!current_user.value) {
    current_user.value = cookies.get('user');
    if (!current_user.value) {
        alert('Please login again to continue, could not find user details');
    }
}

import { v4 as uuidv4 } from 'uuid';

let ticket_data = ref({
    "chat_id": uuidv4(),
    "ticket_id": "SVC-" + uuidv4().replace(/\D/g, '').slice(0, 8),
    "user": current_user.value,
    "medium": "portal",
    "connection": "",
    "text": "",
    "subject": "",
    "summary": "",
    "attachments": [],
    "product_type": "",
    "issue_type": "",
    "priority": "",
    "story_points": "",
    "estimation": "",
    "analysis": "",
    "reply": "",
    "assingee": "",
    "status": "open",
    "created": (new Date()).toISOString(),
    "updated": (new Date()).toISOString(),
    "comments": [
    ],
    "logged_hrs": [
    ]
});

onMounted(() => {
    
    loading.value = true;
    console.log('mounted');
    // fetch(get_incomplete_ticket_url)
    //     .then(response => response.json())
    //     .then(data => {
    //         console.log(data);
    //         ticket_data.value = data;
    //     });
    console.log(ticket_data.value);
    loading.value = false;
});


const auto_fill_url = "http://localhost:5000/text/fill_ticket";
// const auto_fill_url = "http://localhost:5000/get_autofill";
const autoFill = () => {
    if (!ticket_data.value.subject && !ticket_data.value.text) {
        alert('Please fill either the subject or description');
        return;
    }
    loading.value = true;
    console.log('auto-filling form');
    console.log(ticket_data.value);
    fetch(auto_fill_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(ticket_data.value)
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            ticket_data.value = data['result']
            ticket_data.value['status'] = "open";
            console.log(ticket_data.value);
        })
        .finally(() => {
            loading.value = false;
        }); 
};

const reset_form = () => {
    loading.value = true;
    ticket_data.value = {
    "chat_id": uuidv4(),
    "ticket_id": "SVC-" + uuidv4().replace(/\D/g, '').slice(0, 8),
    "user": current_user.value,
    "medium": "portal",
    "connection": "",
    "text": "",
    "subject": "",
    "summary": "",
    "attachments": [],
    "product_type": "",
    "issue_type": "",
    "priority": "",
    "story_points": "",
    "estimation": "",
    "analysis": "",
    "reply": "",
    "assingee": "",
    "status": "open",
    "created": (new Date()).toISOString(),
    "updated": (new Date()).toISOString(),
    "comments": [
    ],
    "logged_hrs": [
    ]
};

    attachments.value = [];
    loading.value = false;
};

let create_url="http://127.0.0.1:5000/text_form";
// let create_url="http://127.0.0.1:5000/ticket/create";


const submitForm = async () => {
    if (!ticket_data.value.subject && !ticket_data.value.text) {
        alert('Please fill either the subject or description');
        return;
    }
    const payload = {
        ...ticket_data.value,
        attachments: attachments.value
    };

    console.log('submitting form:', payload);

    try {
        const response = await fetch(create_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        const result = await response.json();
        console.log(result);
        router.push('/ticket/' + ticket_data.value.ticket_id);
    } catch (error) {
        console.error('Error submitting form:', error);
    }
};






// const submitForm = async () => {
//     const formData = new FormData();
    
//     for (let key in ticket_data.value) {
//         if (Array.isArray(ticket_data.value[key])) {
//             if (key === 'logged_hrs') {
//                 ticket_data.value[key].forEach((item, index) => {
//                     for (let subKey in item) {
//                         formData.append(`${key}[${index}][${subKey}]`, item[subKey]);
//                     }
//                 });
//             } else {
//                 ticket_data.value[key].forEach((item, index) => {
//                     formData.append(`${key}[${index}]`, item);
//                 });
//             }
//         } else {
//             formData.append(key, ticket_data.value[key]);
//         }
//     }
    
//     attachments.value.forEach((file, index) => {
//         formData.append(`files[${index}]`, file); // Adjust this to match backend expectations
//     });


//     console.log('submitting form:', formData);

//     try {
//         const response = await fetch(create_url, {
//             method: 'POST',
//             body: formData
//         });
//         const result = await response.json();
//         console.log(result);
//     } catch (error) {
//         console.error('Error submitting form:', error);
//     }
// };

</script>

<template>
    <LoaderToast :loading="loading" />
    <!-- <NavigationBarView /> -->
    <NavigationBarView2 />
    <div class="home-container">
        <SidePane />
        <div class="main-pane">
            <BreadCrumb :data="bread_path_json" />

            <div class="tile-container ">
                <h1 class="main_title">Create Ticket<div class="ticket_id">{{ ticket_data.ticket_id }}</div></h1>
                <div class="creat_form_cont">
                    <div class="input_cont_2 attach_cont">

                        <div class="input_cont">
                            <label for="title">Title</label>
                            <input type="text" placeholder="Enter your name" class="input_field" id="title" v-model="ticket_data.subject">
                        </div>

                        <button class="btn_cancel ai_button" @click="autoFill">
                            <img src="https://img.icons8.com/?size=100&id=i9i0mLdBTSia&format=png&color=000000"
                                alt="cancel" />Auto Fill
                        </button>

                    </div>

                    <div class="input_cont" v-if="ticket_data.summary">
                        <label for="attachments">Summmary</label>
                        <textarea type="text" placeholder="Summary" class="input_field desc" id="analysis" v-model="ticket_data.summary"
                            style="height: 3vw;"
                            readonly disabled
                            ></textarea>
                    </div>

                    <div class="input_cont">
                        <br>
                        <label for="description">Description</label>
                        <textarea type="text" placeholder="Enter your description" class="input_field desc"
                            id="description" v-model="ticket_data.text" 
                            required
                            ></textarea>
                    </div>


                    <div class="input_cont">

                        <label for="attachments">Analysis</label>
                        <textarea type="text" placeholder="Enter the analysis" class="input_field desc" id="analysis" v-model="ticket_data.analysis"
                            style="height: 4vw;"></textarea>


                        <div class="input_cont_2">
                            <div class="input_cont">
                                <label for="created_by">Created By </label>
                                <input type="text" placeholder="Enter the name of the person" class="input_field"
                                    id="created_by" v-model="ticket_data.user">
                            </div>
                            <div class="input_cont">
                                <label for="assingee">Assigned To</label>
                                <input type="text" placeholder="Enter the name of the person" class="input_field"
                                    id="assingee" v-model="ticket_data.assingee">
                            </div>
                        </div>

                        <div class="input_cont_2">
                            <div class="input_cont">
                                <label for="ticket_type">Ticket Type</label>
                                <select name="ticket_type" class="input_field" id="ticket_type" v-model="ticket_data.issue_type">
                                    <option value="bug">Bug</option>
                                    <option value="feature">Feature</option>
                                    <option value="story">Story</option>
                                    <option value="support">Support</option>
                                    <option value="task">Task</option>
                                    <option value="epic">Epic</option>
                                    <options value="other">Other</options>
                                </select>

                            </div>
                            <div class="input_cont">
                                <label for="priority">Priority</label>
                                <select name="ticket_type" class="input_field" id="ticket_type" v-model="ticket_data.priority">
                                    <option value="low">Low</option>
                                    <option value="medium">Medium</option>
                                    <option value="high">High</option>
                                    <option value="critical">Critical</option>
                                </select>
                            </div>
                        </div>

                        <div class="input_cont_2">
                            <!-- <div class="input_cont">
                    <label for="created_by">Product </label>
                    <input type="text" placeholder="Enter the name of the person" class="input_field" id="created_by">
                </div> -->
                            <div class="input_cont">
                                <label for="ticket_type">Product</label>
                                <select name="ticket_type" class="input_field" id="ticket_type" v-model="ticket_data.product_type" default="other">
                                    <option value="wlpfo">WLPFO</option>
                                    <option value="webgui">WebGUI</option>
                                    <option value="wlsi">WLSI</option>
                                    <option value="ipass">IPASS</option>
                                    <option value="db">DB</option>
                                    <option value="certification">Certification</option>
                                    <option value="testing">Testing</option>
                                    <option value="other">Other</option>
                                </select>

                            </div>
                            <div class="input_cont">
                                <label for="assingee">Status</label>
                                <select  class="input_field" id="assingee" v-model="ticket_data.status" default="open">
                                    <option value="open">Open</option>
                                    <option value="closed">Closed</option>
                                    <option value="pending">Pending</option>
                                    <option value="waiting for information">Waiting for Information</option>    
                                </select>
                            </div>
                        </div>

                        <div class="input_cont_2">

                            <div class="input_cont">
                                <label for="estimation">Estimated Time</label>
                                <input type="number" placeholder="Enter the estimated time" class="input_field"
                                    id="estimation" v-model="ticket_data.estimation" default="1">
                            </div>
                            <div class="input_cont">
                                <label for="ticket_type">Story Points</label>
                                <input type="number" placeholder="Enter the story points" class="input_field"
                                    id="story_points" v-model="ticket_data.story_points" default="1">

                            </div>
                        </div>

                        <div class="input_cont_2 " style="display: flex;
    align-items: flex-start;">
                            <div class="input_cont_2 attach_cont attach_cont_files">
                                <div class="input_cont">
                                    <label for="attachments">Attachments</label>
                                    <input type="file" class="input_field" id="attachments" @change="handleFileChange"
                                        multiple style="display: none;" ref="fileInput">

                                    <button @click="$refs.fileInput.click()" class="btn _attch_but">
                                        Choose Files
                                    </button>

                                    <div class="attachments-list">
                                        <div v-for="(file, index) in attachments" :key="index" class="attachment-item">

                                            <span class="f_size_con">{{ file.name }} <div class="f_size">({{ (file.size
                                                / 1024).toFixed(2) }} KB)</div></span>
                                            <button @click="removeAttachment(index)" class="btn_cancel_file"></button>
                                        </div>
                                    </div>
                                </div>
                            </div>




                            <div class="input_cont_2  last_cno">
                                <button class="btn" @click="submitForm">Create</button>
                                <button class="btn_cancel">
                                    <img src="https://img.icons8.com/ios/50/000000/cancel.png" alt="cancel" />
                                </button>
                                <button class="btn_cancel" @click="reset_form">
                                    <!-- reset -->
                                    <img src="https://img.icons8.com/ios/50/000000/refresh.png" alt="cancel" />
                                </button>
                            </div>
                        </div>

                    </div>


                </div>


            </div>
        </div>

    </div>
</template>

<style scoped>
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
    font-size: 0.9vw;
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
    font-size: 1vw;
}

.tile-container {
    /* margin-top: 2vw; */
    /* width: 80%; */
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    align-items: center;
    justify-content: flex-start;
    /* gap: 1vw; */
    margin-top: 2vw;
    margin: 2vw 4vw;
    width: 70vw;
    margin-bottom: 7vw;
}

.main_title {
    font-family: 'wl2';
    font-size: 2vw;
    font-weight: 900;
    /* width: 90%; */
    width: 80%;
    display: flex;
    flex-direction: row;
    gap: 1vw;
    align-content: center;
    align-items: baseline;
    justify-content: flex-start;
    flex-wrap: nowrap;
}
.ticket_id{
    font-size: 0.8vw;
    font-weight: 100;
    color: rgb(197, 197, 197);
}

.main-pane {
    display: flex;
    align-items: baseline;
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
    font-size: 1vw;
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
.last_cno{
    position: fixed;
    bottom: 0%;
    left: 68%;
    display: -webkit-inline-box;
    gap: 0.5vw;
    padding-bottom: 2vw;
    background-color: white;
}
</style>