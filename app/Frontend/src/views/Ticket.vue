<script setup>
import BreadCrumb from '@/components/BreadCrumb.vue';
import NavigationBarView2 from '@/views/NavigationBarView_2.vue';
import { onMounted, ref } from 'vue';
import SidePane from '@/components/SidePane.vue';
import LoaderToast from '@/components/LoaderToast.vue';
import { faLeaf } from '@fortawesome/free-solid-svg-icons';
import { useRoute } from 'vue-router';
import Sla from '@/components/Sla.vue';
import Activity from '@/components/Activity.vue';

const urlParams = new URLSearchParams(window.location.search);
let ticket_id = urlParams.get('id');

const route = useRoute();
if (!ticket_id) {
    ticket_id = route.params.id;
}

let bread_path_json = {
    "NULLBYTE": "/",
    "TICKETS": "/tickets",
    [`${ticket_id}`]: "/ticket?id=${ticket_id}",
};

// const attachments = ref([]);

// const handleFileChange = (event) => {

//     loading.value = true;
//     const files = Array.from(event.target.files);
//     attachments.value.push(...files);

//     event.target.value = '';

//     loading.value = false;
// };

// const removeAttachment = (index) => {
//     attachments.value.splice(index, 1);
// };


const loading = ref(true);

const get_ticket_url = "http://localhost:5000/get_ticket";
const get_incomplete_ticket_url = "http://localhost:5000/get_incomplete_ticket";
// const auto_fill_url = "http://localhost:5000/text/fill_ticket";
const auto_fill_url = "http://localhost:5000/get_autofill";



let ticket_data = ref({
    "chat_id": "",
    "ticket_id": "",
    "user": "",
    "medium": "",
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
    "status": "",
    "created": "",
    "updated": "",
    "comments": [
    ],
    "logged_hrs": [
    ]
});

onMounted(() => {
    loading.value = true;
    console.log('mounted');
    fetch(get_incomplete_ticket_url)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            ticket_data.value = data;
            console.log(ticket_data.value.comments);
            refreshComponent();
        })
        .finally(() => {
            loading.value = false;
        });

    console.log(ticket_data.value);

    autoFill();

    let doc_tetx = document.getElementById('desc_te');
    if (doc_tetx.scrollHeight <= 200) {
        doc_tetx.style.height = 'auto';
        doc_tetx.style.height = doc_tetx.scrollHeight + 'px';
    }

    autoFill();
    extract_links();
    // sla_json_data.value.estimated = ticket_data.value.estimation;
});

const componentKey = ref(0); // A key that will trigger a re-render when changed

const refreshComponent = () => {
    componentKey.value += 1; // Changing the key forces the component to re-render
};

const autoFill = () => {
    loading.value = true;

    console.log(attachments.value.length);
    fetch(auto_fill_url)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            ticket_data.value = data;
            get_attachments_from_data();
            extract_links();
        });
};

const reset_form = () => {
    loading.value = true;
    ticket_data.value = {
    "chat_id": ticket_data.value.chat_id,
    "ticket_id": ticket_data.value.ticket_id,
    "user": ticket_data.value.user,
    "medium": ticket_data.value.medium,
    "connection": "",
    "text": ticket_data.value.text, 
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
    "created": ticket_data.value.created,
    "updated": "",
    "comments": ticket_data.value.comments,
    "logged_hrs": []
};

    attachments.value = [];
    loading.value = false;
};

function formatDate(date) {
    // convert from 2021-07-15T10:00:00 to Friday, 7th July 2021
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(date).toLocaleDateString('en-GB', options);

}

function autoExpand(event) {
    const textarea = event.target;
    if (textarea.scrollHeight <= 200) {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    }

}


// Reactive attachment list
const attachments = ref([]);
// get attachments from ticket_data.attachments
// attachments.value = ticket_data.value.attachments;
// example : 

function get_attachments_from_data() {
    const newAttachments = ticket_data.value.attachments.map(file => ({
        name: file.name,
        type: file.type,
        size: file.size,
        url: file.url,
        details: file.details
    }));
    // check if same url exists in attachments
    // if not add it to attachments
    if (attachments.value.length > 0) {
        newAttachments.forEach((newAttachment) => {
            const exists = attachments.value.some((attachment) => attachment.url === newAttachment.url);
            if (!exists) {
                attachments.value.push(newAttachment);
            }
        });
    } else {
        attachments.value = [...attachments.value, ...newAttachments];
    }
}



// Ref for file input element
const fileInput = ref(null);

function check_padd(){
    if (attachments.value.length > 2) {
        document.querySelector('.attach_cont').style.display = 'flex';
        document.querySelector('.attach_cont').style.flexDirection = 'row';
        document.querySelector('.attach_cont').style.alignItems = 'stretch';
        document.querySelector('.attach_cont').style.alignContent = 'center';
        document.querySelector('.attach_cont').style.flexWrap = 'wrap';
        document.querySelector('.attach_cont').style.justifyContent = 'center';
        document.querySelector('.attachments-list').style.marginTop = '-0.8rem';
        
    }
    else {
        document.querySelector('.attach_cont').style.display = 'flex';
        document.querySelector('.attach_cont').style.flexDirection = 'row';
        document.querySelector('.attach_cont').style.alignItems = 'center';
        document.querySelector('.attach_cont').style.alignContent = 'space-between';
        document.querySelector('.attach_cont').style.flexWrap = 'wrap';
        document.querySelector('.attach_cont').style.justifyContent = 'center';
        document.querySelector('.attachments-list').style.marginTop = '-0rem'; 
    }
}

// Handle file input change
const handleFileChange = (event) => {
    const newFiles = Array.from(event.target.files);
    const newAttachments = newFiles.map(file => ({
        name: file.name,
        type: file.type,
        size: file.size,
        url: URL.createObjectURL(file),
        details: null

    }));

    attachments.value = [...attachments.value, ...newAttachments];
    check_padd();

};

const removeAttachment = (index) => {
    URL.revokeObjectURL(attachments.value[index].url);
    attachments.value.splice(index, 1);
    check_padd();
};

const getFileTitle = (file) => {
    return `Filename: ${file.name}\nSize: ${(file.size / 1024).toFixed(2)} KB\nType: ${file.type}\nURL: ${file.url}\nDetails: ${file.details}`;
};

let links=ref([]);

function extract_links() {  
    const text = ticket_data.value.text;
    const summary = ticket_data.value.summary;
    const comments = ticket_data.value.comments;
    const linksArray = [];
    const link_pattern = /((http|https):\/\/[^\s]+|www\.[^\s]+)/g; 
    if (text) {
        linksArray.push(...(text.match(link_pattern) || []));
    }

    if (summary) {
        linksArray.push(...(summary.match(link_pattern) || []));
    }
    comments.forEach(comment => {
        if (comment.text) {
            linksArray.push(...(comment.text.match(link_pattern) || []));
        }
    });
    links.value = [...new Set(linksArray)];
}

let sla_json_data = ref({
    "estimated": 0,
    "logged":0 ,
})

function total_logged_hrs(){
    let total = 0;
    ticket_data.value.logged_hrs.forEach(log => {
        total += log.logged;
    });
    alert(total);
    return total;
}
 

const handleAddComment = (newCommentText) => {
  const newComment = {
    comment_id: ticket_data.value.comments.length + 1, // Generate a unique ID for the new comment
    user: 'CurrentUser', // Replace with dynamic user if needed
    text: newCommentText,
    date: new Date().toISOString() // Capture the current date
  };

  // Add the new comment to the comments array
  ticket_data.value.comments.push(newComment);
};

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
                <h1 class="main_title">{{ ticket_data.ticket_id }}:<div class="ticket_id">{{ ticket_data.subject }}
                    </div>
                </h1>
                <div class="cont_paral">
                    <div class="bold_text_banner">{{ formatDate(ticket_data.created) }}</div>
                    <select v-model="ticket_data.status" :class="{
                        'bold_text_banner banner_drop ban_dropp': true,
                        'banner_open': ticket_data.status.toLowerCase() === 'open',
                        'banner_closed': ticket_data.status.toLowerCase() === 'closed',
                        'banner_waiting': ticket_data.status.toLowerCase() === 'waiting for information'
                    }">
                        <option value="open">Open</option>
                        <option value="closed">Closed</option>
                        <option value="waiting for information">Waiting for Information</option>
                    </select>
                </div>
                <div class="tick_info">
                    <div class="typ_info">
                        <div class="tinfo_text" >
                            <div>Type&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:</div> &nbsp;
                            <select class="typ_inp drop_inpt" v-model="ticket_data.issue_type" :class="{ 'inp_desc_none': !ticket_data.issue_type }" >
                                <option value="bug">Bug</option>
                                <option value="feature">Feature</option>
                                <option value="story">Story</option>
                                <option value="support">Support</option>
                                <option value="task">Task</option>
                                <option value="epic">Epic</option>
                            </select>
                        </div>
                        <div class="tinfo_text">
                            <div>Priority&nbsp;&nbsp;:</div>&nbsp;
                            <select class="typ_inp drop_inpt" v-model="ticket_data.priority" :class="{ 'inp_desc_none': !ticket_data.priority }">
                                <option value="low">Low</option>
                                <option value="medium">Medium</option>
                                <option value="high">High</option>
                                <option value="critical">Critical</option>
                            </select>
                        </div>
                    </div>
                    <hv></hv>
                    <div class="typ_info">
                        <div class="tinfo_text">
                            <div>Created By&nbsp;&nbsp;&nbsp;&nbsp;:</div> &nbsp;&nbsp;
                            <!-- <div class="typ_inp">{{ ticket_data.user }}</div> -->
                            <input type="text" placeholder="Add Username" class="input_field drop_inpt drop_input_tex"
                                id="created_by" v-model="ticket_data.user" readonly disabled :class="{ 'inp_desc_none': !ticket_data.user }" >
                        </div>

                        <div class="tinfo_text">
                            <div>Assigned To&nbsp;&nbsp;:</div>&nbsp;
                            <input type="text" placeholder="Add Username" class="input_field drop_inpt drop_input_tex"
                                id="assingee" v-model="ticket_data.assingee" :class="{ 'inp_desc_none': !ticket_data.assingee }">
                        </div>
                    </div>
                    <hv></hv>
                    <div class="typ_info">
                        <div class="tinfo_text">
                            <div>Product&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:</div> &nbsp;
                            <select class="typ_inp drop_inpt" v-model="ticket_data.product_type" :class="{ 'inp_desc_none': !ticket_data.product_type }">
                                <option value="wlpfo">WLPFO</option>
                                <option value="webgui">WebGUI</option>
                                <option value="wlsi">WLSI</option>
                                <option value="ipass">IPASS</option>
                                <option value="db">DB</option>
                                <option value="certification">Certification</option>
                                <option value="testing">Testing</option>
                            </select>
                        </div>
                        <div class="tinfo_text">
                            <div>Story Points &nbsp;:</div> &nbsp;
                            <input class="typ_inp drop_inpt drop_inpt_num" v-model="ticket_data.story_points"
                                type="number" name="story_points" id="story_points" range="0" min="0" max="100"
                                step="1" :class="{ 'inp_desc_none': !ticket_data.story_points }">
                        </div>
                    </div>

                </div>
                <div class="both_tog">
    <div class="first_part">
        <div class="input_cont">
            <label for="desc_te" class="inpt_desc_lab">Description</label>
            <textarea placeholder="Enter your name" class="input_field inp_desc" 
                      :class="{ 'inp_desc_none': !ticket_data.text }" id="desc_te"
                      v-model="ticket_data.text" @input="autoExpand;extract_links()">
            </textarea>
        </div>

        <div class="input_cont con_spl" v-if="ticket_data.summary">
            <label for="summary_te" class="inpt_desc_lab">Summary</label>    
            <textarea placeholder="Enter Summary" class="input_field inp_desc" 
                      id="summary_te" v-model="ticket_data.summary" @input="autoExpand" readonly disabled>
            </textarea>
        </div>

        <div class="input_cont con_spl">
            <label for="title" class="inpt_desc_lab">Attachments</label>
            <div class="input_cont attach_cont_files">
                <div class="input_cont attach_cont">
                    <input type="file" class="input_field att" id="attachments" 
                           @change="handleFileChange" multiple style="display: none;" ref="fileInput">

                    <button @click="$refs.fileInput.click()" class="btn _attch_but">
                        <div>+</div>
                    </button>

                    <div class="attachments-list">
                        <div v-for="(file, index) in attachments" :key="index" class="attachment-item" 
                             :title="getFileTitle(file)">
                            <div class="attachment-preview">
                                <img v-if="file.type.includes('image')" :src="file.url || URL.createObjectURL(file)" 
                                     class="attachment-img" />
                                <span v-else class="attachment-icon">📄</span>
                            </div>
                            <div class="attachment-info">
                                <span class="file-name">{{ file.name }}</span>
                                <div class="file-size">({{ (file.size / 1024).toFixed(2) }} KB)</div>
                            </div>
                            <button @click="removeAttachment(index)" class="btn_cancel_file">❌</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="input_cont con_spl" v-if="links.length > 0">
            <label for="links" class="inpt_desc_lab">Links</label>
            <div v-for="(link, index) in links" :key="index" class="links-item">
                <a :href="link.startsWith('http') ? link : `http://${link}`" target="_blank">{{ link }}</a>
            </div>
        </div>


        <div class="creat_form_cont">
                    <div class="input_cont_2 attach_cont">
                    </div>

                    <!-- <div class="input_cont" v-if="ticket_data.summary">
                        <label for="attachments">Summmary</label>
                        <textarea type="text" placeholder="Summary" class="input_field desc" id="analysis"
                            v-model="ticket_data.summary" style="height: 3rem;" readonly disabled></textarea>
                    </div>

                    <div class="input_cont">
                        <label for="description">Description</label>
                        <textarea type="text" placeholder="Enter your description" class="input_field desc"
                            id="description" v-model="ticket_data.text" required></textarea>
                    </div> -->



                        <!-- <label for="attachments">Analysis</label>
                        <textarea type="text" placeholder="Enter the analysis" class="input_field desc" id="analysis"
                            v-model="ticket_data.analysis" style="height: 4rem;"></textarea> -->


                        <div class="input_cont_2 " style="display: flex;
    align-items: flex-start;">





                            <div class="input_cont_2 but_con al_but">
                                <button class="btn">Move To Jira</button>
                                <button class="btn_cancel">
                                    <img src="https://img.icons8.com/ios/50/000000/save.png">
                                </button>
                                <button class="btn_cancel" @click="reset_form">
                                    <!-- reset -->
                                    <img src="https://img.icons8.com/ios/50/000000/refresh.png" alt="cancel" />
                                </button>
                            </div>
                        </div>



                </div>
    </div>

    <div class="second_part">
        <div class="input_cont input_contsec" style="margin-top: 0rem;">
            <label for="analysis" class="inpt_desc_lab sprint_ti">Sprint Progress
            </label>
                <Sla :logged_hrs="ticket_data.logged_hrs" :estimated_hrs="ticket_data.estimation" />
                <vv><vvv></vvv></vv>
            <label for="analysis" class="inpt_desc_lab sprint_ti">Activity
                <button class="btnsort"><img src="https://img.icons8.com/?size=100&id=1701&format=png&color=000000" />
                </button>
            </label>
            <Activity :comments="ticket_data.comments" @addComment="handleAddComment" />

        </div>  

    </div>
</div>




            </div>
        </div>

    </div>
</template>

<style scoped>
vv{
    width: 20rem;
    height: 0.1rem;
    /* background-color: #81818175; */
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 0.2rem;
    margin-bottom: 1rem;
}
vvv{
    width: 70%;
    background-color: #81818122;
    height: 0.1rem;
}
.btnsort {
    color: white;

    /* padding: 0.1rem 0rem; */
    border: none;
    border-radius: 0.3rem;
    cursor: pointer;
    text-align: center;
    margin: auto;
    height: 1.4 rem;
    width: 1.7rem;
    padding-top: 0.2rem;
    margin-left: 0.6rem;
    transform: scale(0.8);
}

.btnsort:hover { 
    background-color: #46BEAA;
}

.btnsort:hover img {
    filter: invert(1);
}

.btnsort img {
    width: 1rem;
    height: 1rem;
    filter: invert(0.5);
}
.second_part {
    width: -webkit-fill-available;
    margin-left: 0rem;
    border-left: 0.1rem solid #81818117;
    position: fixed;
    top: 21%;
    left: 76%;
    background: white;
    width: auto;
}
.input_contsec{
    margin-left: 1rem;
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
    margin-bottom: 1rem;
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
    justify-content: flex-start;
    /* gap: 1rem; */
    margin-top: 2rem;
    /* margin: 2rem 4rem; */
    width: 70vw;
    height: 100%;
    margin-bottom: 7rem;
}

.main_title {
    font-family: 'wl2';
    font-size: 2rem;
    font-weight: 900;
    /* width: 90%; */
    /* width: 80%; */
    display: flex;
    flex-direction: row;
    gap: 1rem;
    align-content: center;
    align-items: baseline;
    justify-content: flex-start;
    flex-wrap: nowrap;
    width: -webkit-fill-available;
    margin-left: 7rem;
    white-space: nowrap;
}

.ticket_id {
    font-size: 1.7rem;
    font-weight: 500;
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
    flex-flow: wrap;
    align-items: baseline;
    place-content: space-between center;
    justify-content: center;
    align-content: center;
    flex-wrap: nowrap;
    flex-direction: row;
}

.attach_cont_files {
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    align-items: flex-start;
    justify-content: center;
    margin-top: 0rem;
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
    gap: 2rem;
    justify-content: flex-end;
    
}

.attachment-item:hover {
    background-color: #f0f0f0;
    cursor: pointer;
}

.attachments-list {
    margin-top: 0rem;
    font-size: 0.8rem;

}

.btn_cancel_file {
    padding: 0rem 0rem;
    color: rgba(77, 4, 4, 0.557);
    background-color: white;
    border: 0.05rem solid rgb(77, 4, 4);
    border-radius: 0.3rem;
    cursor: pointer;
    filter: saturate(0.3);
}

.btn_cancel_file:hover {
    /* background-color: rgb(208, 44, 44); */
    color: white;
    filter: saturate(1);
}

/* .btn_cancel_file::after {
    content: 'X';
} */

._attch_but {
    background-color: grey;
    border-color: white;
    margin-top: 0.6rem;
}

._attch_but:hover {
    background-color: rgb(65, 65, 65);
    border-color: white;
    color: white;
    border: 0.1rem solid #81818175;
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

.cont_paral {
    display: flex;
    gap: 1.4rem;
    width: -webkit-fill-available;
    margin-left: 7rem;
    margin-top: 0.4rem;
}

.bold_text_banner {
    background-color: rgb(84, 84, 84);
    padding: 0.1rem 1.5rem;
    border-radius: 0.4rem;
    color: white;
    font-size: 0.8rem;
    text-align: center;
}

.banner_drop {
    background-color: rgb(84, 84, 84);
}

.banner_open {
    background-color: rgb(210, 183, 30);
}

.banner_closed {
    background-color: var(--wl);

}

.banner_waiting {
    background-color: #0057a4;
}

.tick_info {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: flex-start;
    align-items: center;
    width: 100%;
    margin-left: 16rem;
    margin-top: 1rem;
    gap: 2rem;
    font-family: wl1;
    color: rgb(158, 158, 158);
    font-size: 0.8rem;
}

hv {
    width: 0.08rem;
    height: 2rem;
    background-color: rgba(158, 158, 158, 0.4);
}

.typ_info {
    display: flex;
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: center;
    align-items: baseline;
    gap: 0.5rem;
}

.tinfo_text {
    display: flex;
}

.typ_inp {
    cursor: pointer;
    opacity: 0.9;
    text-transform: capitalize;
}

.tinfo_text {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: center;
    align-items: center;
}

.drop_inpt {
    cursor: pointer;
    opacity: 0.9;
    text-transform: capitalize;
    width: 6rem;
    border: none;
    padding: 0;
    margin: 0;
    width: webkit-fill-available;
    background-color: transparent;
    font-size: 0.8rem;
    color: black;
    font-family: wl1;
}

.drop_inpt:hover {
    background-color: #f0f0f0;
}

.drop_inpt:focus {
    outline: none;
    border: none;
}

.drop_inpt_num {
    cursor: initial;
    padding: 0rem 0rem 0rem 0.2rem;
    width: 5.6rem;
}

.drop_input_tex {
    cursor: initial;
    padding: 0rem 0rem 0rem 0.2rem;
    width: 4.8rem;
}

.drop_input_tex:focus {
    outline: none;
    border: none;
}

.drop_input_tex:hover {
    background-color: #f0f0f0;
}

.drop_input_tex::placeholder {
    font-size: 0.8rem;
}

.drop_input_tex:disabled:hover {
    cursor: not-allowed;
    background-color: #ffffff;
}

.ban_dropp {
    width: 10rem !important;
    text-align: center;
    text-align-last: center;
    margin-top: 0rem;
    text-transform: capitalize;
}

.inp_desc {
    width: 100%;
    height: 1.5rem;
    min-height: 1.5rem;
    border: 0.1rem solid #81818100;
    border-radius: 0.3rem;
    padding: 0.5rem;
    margin-top: 0.5rem;
    font: 0.9rem 'wl1';
    word-spacing: 0.1rem;
    /* line-height: 1.5rem; */
    color: black;
    min-width: 40rem;
    max-width: 45rem;
    /* height: 5rem; */
}

.inp_desc:hover {
    cursor: pointer;
    /* border: 0.1rem solid #c8c8c8 */
    background-color: #f0f0f093;
}
.inp_desc_none{
    background-color: #f0f0f093;
}

.inp_desc:focus {
    outline: none;
    cursor: text;
    border: 0.1rem solid #c8c8c8;
}

.inp_desc::-webkit-scrollbar {
    width: 0.4rem;
    height: 0.5rem;
}

.inp_desc::-webkit-scrollbar-thumb {
    background-color: #c8c8c8;
    border-radius: 0.3rem;
}

.inp_desc::-webkit-scrollbar-track {
    background-color: #f0f0f0;
}

.inp_desc::-webkit-scrollbar-thumb:hover {
    background-color: #c8c8c8;
}

.inpt_desc_lab {
    font-size: 1.4rem;
    font-family: wl2;
    color: #393939;
    margin-top: 0.5rem;
}

.both_tog {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: space-between;
    align-items: baseline;
    width: 100%;
    margin-left: 5rem;
    margin-top: 1rem;
    gap: 7rem;
}

.first_part {
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: space-between;
    align-items: baseline;
    width: 100%;
    /* margin-left: 16rem; */
    /* margin-top: 1rem; */
    gap: 0rem;
}

.con_spl {
    border-top: 0.1rem solid #8181813d;
    margin-top: 1.8rem;
    /* margin-bottom: 1rem; */
    padding-top: 0.8rem;
    width: 40vw;
}

._attch_but {
    height: 3rem;
    width: 3rem;
    padding: 0;
    font-size: 1.6rem;
    background-color: rgba(214, 214, 214, 0.1);
    border-radius: 0.2rem;
    border: 0.1rem solid #81818143;
    margin-top: 0rem;
    display: flex;
    flex-wrap: nowrap;
    align-content: center;
    align-items: center;
    justify-content: center;
    flex-direction: row;
    color: white !important;
}

._attch_but * {
    color: rgb(120, 120, 120);
}

._attch_but:hover * {
    /* rotate the inner text 180deg */
    transform: rotate(360deg);
    color: white;
}

.attachments-list {
    display: flex;
    flex-direction: row;
    max-width: 35rem;
    gap: 2rem;
    row-gap: 1rem;
    flex-wrap: wrap;
    align-content: flex-start;
    justify-content: flex-start;
    align-items: flex-start;
    transform: scale(0.8);
    /* height: 3rem; */
}

.attachment-item {
    flex: 1 1 calc(50% - 2rem);
    box-sizing: border-box;
}

.attachment-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border: 0.1rem solid #ccc;
    border-radius: 0.3rem;
    padding: 0.5rem;
    margin-bottom: 0rem;
    width: 100%;

    max-width: 16rem;
    margin-top: 0rem;
    /* padding: 0rem 1  rem; */
}

.attachment-preview {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2.5rem;
    height: 2.5rem;
    border: 0.1rem solid #ddd;
    border-radius: 0.3rem;
    overflow: hidden;
}

.attachment-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.attachment-icon {
    font-size: 1rem;
    color: #666;
}

.attachment-info {
    flex-grow: 1;
    margin-left: 0rem;
}

.file-name {
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 7rem;
    width: 20rem;
    display: block;
}

.file-size {
    font-size: 0.6rem;
    color: #777;
}

.file-details {
    font-size: 0.6rem;
    color: #555;
    margin-top: 0rem;
}

.btn_cancel_file {
    background: none;
    border: none;
    font-size: 0.7rem;
    cursor: pointer;
    padding-left: 0.3rem;
    color: #ff0000;
}


.att {
    display: flex;
    flex-direction: row;
}

textarea:disabled {
    cursor: not-allowed !important;
}

.links-item{
    margin-top: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.7rem;
}
.links-item a{
    color: rgb(27, 86, 205);
    text-decoration: none;
}
.links-item:hover{
    text-decoration: underline;
}
.sprint_ti{font-size: 1rem;
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: center;
    align-items: center;
}
.al_but{
    position: fixed;
    bottom: 0%;
    background: white;
    padding-bottom: 2.1rem;
    margin-top: 0rem;
    margin-bottom: 0rem;
    width: -webkit-fill-available;
}

</style>