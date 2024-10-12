<script setup>
import BreadCrumb from '@/components/BreadCrumb.vue';
import NavigationBarView2 from '@/views/NavigationBarView_2.vue';
import { ref } from 'vue';
import SidePane from '@/components/SidePane.vue';

let bread_path_json = {
    "NULLBYTE": "/",
    "TICKETS": "/tickets",
    "CREATE TICKET": "/create_ticket",
};

const attachments = ref([]);

const handleFileChange = (event) => {
    const files = Array.from(event.target.files);
    attachments.value.push(...files);

    event.target.value = '';
};

const removeAttachment = (index) => {
    attachments.value.splice(index, 1);
};
</script>


<template>

    <!-- <NavigationBarView /> -->
    <NavigationBarView2 />
    <div class="home-container">
        <SidePane />
        <div class="main-pane">
            <BreadCrumb :data="bread_path_json" />

            <div class="tile-container ">
                <h1 class="main_title">Create Ticket</h1>
                <div class="creat_form_cont">
                    <div class="input_cont_2 attach_cont">

                        <div class="input_cont">
                            <label for="title">Title</label>
                            <input type="text" placeholder="Enter your name" class="input_field" id="title">
                        </div>

                        <button class="btn_cancel ai_button">
                            <img src="https://img.icons8.com/?size=100&id=i9i0mLdBTSia&format=png&color=000000"
                                alt="cancel" />Auto Fill
                        </button>

                    </div>

                    <div class="input_cont">
                        <label for="description">Description</label>
                        <textarea type="text" placeholder="Enter your description" class="input_field desc"
                            id="description"></textarea>
                    </div>

                    <div class="input_cont">
                        <label for="attachments">Analysis</label>
                        <textarea type="text" placeholder="Enter the analysis" class="input_field desc"
                            id="analysis"></textarea>


                        <div class="input_cont_2">
                            <div class="input_cont">
                                <label for="created_by">Created By </label>
                                <input type="text" placeholder="Enter the name of the person" class="input_field"
                                    id="created_by">
                            </div>
                            <div class="input_cont">
                                <label for="assingee">Assigned To</label>
                                <input type="text" placeholder="Enter the name of the person" class="input_field"
                                    id="assingee">
                            </div>
                        </div>

                        <div class="input_cont_2">
                            <div class="input_cont">
                                <label for="ticket_type">Ticket Type</label>
                                <select name="ticket_type" class="input_field" id="ticket_type">
                                    <option value="bug">Bug</option>
                                    <option value="feature">Feature</option>
                                    <option value="story">Story</option>
                                    <option value="support">Support</option>
                                    <option value="task">Task</option>
                                    <option value="epic">Epic</option>
                                </select>

                            </div>
                            <div class="input_cont">
                                <label for="priority">Priority</label>
                                <select name="ticket_type" class="input_field" id="ticket_type">
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
                                <select name="ticket_type" class="input_field" id="ticket_type">
                                    <option value="wlpfo">WLPFO</option>
                                    <option value="webgui">WebGUI</option>
                                    <option value="wlsi">WLSI</option>
                                    <option value="ipass">IPASS</option>
                                    <option value="db">DB</option>
                                    <option value="certification">Certification</option>
                                    <option value="testing">Testing</option>
                                </select>

                            </div>
                            <div class="input_cont">
                                <label for="assingee">Assigned To</label>
                                <input type="text" placeholder="Enter the name of the person" class="input_field"
                                    id="assingee">
                            </div>
                        </div>

                        <div class="input_cont_2">

                            <div class="input_cont">
                                <label for="estimation">Estimated Time</label>
                                <input type="number" placeholder="Enter the estimated time" class="input_field"
                                    id="estimation">
                            </div>
                            <div class="input_cont">
                                <label for="ticket_type">Story Points</label>
                                <input type="number" placeholder="Enter the story points" class="input_field"
                                    id="story_points">

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




                            <div class="input_cont_2 but_con">
                                <button class="btn">Create</button>
                                <button class="btn_cancel">
                                    <img src="https://img.icons8.com/ios/50/000000/cancel.png" alt="cancel" />
                                </button>
                                <button class="btn_cancel">
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
    justify-content: center;
    /* gap: 1rem; */
    margin-top: 2rem;
    margin: 2rem 4rem;
    width: 70vw;
    margin-bottom: 7rem;
}

.main_title {
    font-family: 'wl2';
    font-size: 2rem;
    font-weight: 900;
    /* width: 90%; */
    width: 80%;
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
</style>