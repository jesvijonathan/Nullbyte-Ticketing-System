<script setup>
import { useAuthStore } from '@/stores/auth';
import Tile from '@/components/Tile.vue';
import SidePane from '@/components/SidePane.vue';
import router from '../router';
import BreadCrumb from '@/components/BreadCrumb.vue';
import NavigationBarView from '@/views/NavigationBarView.vue';
import NavigationBarView2 from '@/views/NavigationBarView_2.vue';
import ChatbotImg from '@/assets/chatbot.svg';
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { io } from 'socket.io-client';
import { useCookies } from 'vue3-cookies';
import { faL } from '@fortawesome/free-solid-svg-icons';

// Socket connection
const baseSocketURL = document.baseSocketURL || 'http://localhost'; // Ensure this is defined
const socket = io(baseSocketURL, {
    transports: ['websocket'],
});
console.log("@@@@ BaseUri", document.baseSocketURL, document.baseMyURL);
console.log("@@@@socket", socket);

const current_user = ref(null);
const { cookies } = useCookies();
const authStore = useAuthStore();

let bread_path_json = {
    "NULLBYTE": "/",
    "CHATBOT": "/chatbot",
    "VERTEX AI": "/vertex"
};

// Message and attachment handling
let convo = ref([]);
let waiting_for_response = ref(false);
const messageInput = ref('');
const fileInput = ref(null);
const clipboardAttachments = ref([]);
const attachments = ref([]);
const sentAttachments = ref([]);
const attachmentContainer = ref([]);
const closed_chat = ref({});
let convoArray = Object.entries(convo).filter(([key, value]) => key !== "ticket_id");

if (!current_user.value) {
    current_user.value = cookies.get('user');
    if (!current_user.value) {
        alert('Please login again to continue, could not find user details');
    }
}

const getFileTitle = (file) => {
    return `Filename: ${file.name}\nSize: ${(file.size / 1024).toFixed(2)} KB\nType: ${file.type}\nURL: ${file.url}\nDetails: ${file.details}`;
};

const removeAttachment = (index) => {
    URL.revokeObjectURL(attachments.value[index].url);
    attachments.value.splice(index, 1);
    // check_padd();
};

// On component mount
let connected = ref(false)

onMounted(() => {
    const convoContainer = document.querySelector('.convo');
    convoContainer.scrollTop = convoContainer.scrollHeight;

    socket.on('connect', () => {
        connected.value = true
        console.log('Connected to server');
    });

    socket.on('disconnect', () => {
        connected.value = false
        console.log('Disconnected from server');
    });

    socket.on('response', (data) => {
        console.log('Response data:', data);
        addMessageToChat('Bot', data.message);
    });

    socket.on('close_chat', (data) => {
        console.log('Chat closed:', data['closed_chat']);
        closed_chat.value = data["closed_chat"];    
        return
        // socket.disconnect();
    });

    socket.on('live_chat', (data) => {
        console.log('Live chat data:', data);
        if (!data || !data.live_chat) return;
        convo.value = data.live_chat;
        waiting_for_response = false
        const convoContainer = document.querySelector('.convo');
        convoContainer.scrollTop = convoContainer.scrollHeight; 
        // print last message
        if (convo.value){
            if (convo.value[Object.keys(convo.value).length].recipient == "wl_vertex"){
                if (window.location.href.includes("llama")){
                    sendMessage("/change");
                }
            }
            else if(convo.value[Object.keys(convo.value).length].recipient == "wl_llama"){
                if (window.location.href.includes("vertex")){
                    sendMessage("/change");
                }
            }
            else{
                if (convo.value[Object.keys(convo.value).length - 1].message == "/change"){

                }
                else{
                if (convo.value[Object.keys(convo.value).length - 1].recipient == "wl_vertex"){
                    if (window.location.href.includes("llama")){
                    sendMessage("/change");
                }
                }
                else if(convo.value[Object.keys(convo.value).length - 1].recipient == "wl_llama"){
                    if (window.location.href.includes("vertex")){
                    sendMessage("/change");
                }
                }
            }
            }
        }
    });

    socket.on('user_attachment_received', (attachment) => {
        console.log('Attachment received:', attachment);
        const message = `Attachment received: ${attachment.file_name} (${attachment.size_mb} MB)`;
        addMessageToChat('Bot', message);
    });


    convoContainer.scrollTop = convoContainer.scrollHeight;
});

socket.on('connect_error', function (err) {
    console.error('Connection failed:', err);
});

socket.on('connect_timeout', function (err) {
    console.error('Connection timed out:', err);
});

socket.on('error', function (err) {
    console.error('Error:', err);
});

// Function to handle sending messages and attachments
function sendMessage(msg = "") {
    // print current history 
    console.log('Current convo:', convo.value);
    waiting_for_response = true;
    if (msg != null) {
        messageInput.value = msg;
    }
    
    if (messageInput.value == '/change') {
        if (bot == "Vertex AI") {
            bot = "Llama AI";
        } else {
            bot = "Vertex AI";
        }
    }

    // "recipient": "admin",
    //     "time": "2024-10-09T21:53:28.668620",
    //     "message": "hello i have an issue logging in.. .can you check ?",
    //     "attachment": {
    //         "0": {
    //             "filename": "log.txt",
    //             "path": "./bucket/chats/dXF-PzYcYbANChgkAAAF/log.txt",
    //             "extension": "txt",
    //             "mime_type": "text/plain",
    //             "size": 4382
    //         },
    //         "1": {
    //             "filename": "Invalid_LoginID.jpg",
    //             "path": "./bucket/chats/dXF-PzYcYbANChgkAAAF/Invalid_LoginID.jpg",
    //             "extension": "jpg",
    //             "mime_type": "image/jpeg",
    //             "size": 31031
    //         }
    //     }
    

    const message = messageInput.value;
    const files = fileInput.value ? fileInput.value.files : [];
    const tmpAttachments = JSON.parse(JSON.stringify([...attachments.value, ...clipboardAttachments.value]));

    convo.value = {
        ...convo.value,
        [Object.keys(convo.value).length + 1]: {
            recipient: current_user.value,
            time: new Date().toISOString(),
            message: messageInput.value,
            attachments: tmpAttachments.length ? tmpAttachments : undefined
        }
    };

    console.log('attach1:', attachments.value);
    console.log('attach2:', tmpAttachments);
    console.log('attach3:', clipboardAttachments.value);

    attachments.value = [];
    clipboardAttachments.value = [];

    console.log('Files:', files);
    console.log('Attachments:', tmpAttachments);
    console.log('Message:', message);

    if (message || tmpAttachments.length || files.length) {
        const filePromises = [...files].map(file => readFile(file));

        Promise.all(filePromises).then((fileAttachments) => {
            // tmpAttachments.push(...fileAttachments);
            sendToServer(message, tmpAttachments);
            clipboardAttachments.value = [];
            attachmentContainer.value = '';
            messageInput.value = '';
        });
    }

    sentAttachments.value = [...tmpAttachments];

    const convoContainer = document.querySelector('.convo');
    convoContainer.scrollTop = convoContainer.scrollHeight;

    setTimeout(() => {
        convoContainer.scrollTop = convoContainer.scrollHeight;
    }, 400);
}

function readFile(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => {
            const attachment = {
                name: file.name,  // Change 'file_name' to 'name'
                size: file.size,  // Ensure 'size' is passed
                type: file.type,  // Include the type for images
                url: URL.createObjectURL(file),  // You might need the URL for preview
                data: reader.result.split(',')[1]  // Keep this if you need base64 data
            };
            resolve(attachment);
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}


function sendToServer(message, attachments) {
    if (message) addMessageToChat('You', message);
    attachments.forEach((attachment) => {
        addMessageToChat('You', `Attachment: ${attachment.file_name} (${attachment.size_mb} MB)`);
    });

    socket.emit('user_attachment', { message, attachments });
}

function addMessageToChat(sender, message) {
    // if (Array.isArray(convo.value)) {
    //     convo.value.push({ recipient: sender, message, time: new Date().toISOString() });
    // } else {
    //     convo.value = [{ recipient: sender, message, time: new Date().toISOString() }];
    // }
}

// Handle file input change
function handleFileInput(event) {
    const files = event.target.files;
    if (files.length) {
        const filePromises = [...files].map(file => readFile(file));
        Promise.all(filePromises).then((fileAttachments) => {
            attachments.value.push(...fileAttachments);
            console.log('Selected files:', attachments.value);
        }).catch(error => {
            console.error('Error reading files:', error);
        });
    }
    console.log('Files selected:', attachments);
}

// Function to handle paste events for attachments
document.addEventListener('paste', (event) => {
    const items = event.clipboardData.items;
    for (let i = 0; i < items.length; i++) {
        if (items[i].kind === 'file') {
            const file = items[i].getAsFile();
            handleFileUpload(file);
        }
    }
});

function handleFileUpload(file) {
    readFile(file).then(attachment => {
        clipboardAttachments.value.push(attachment);
    }).catch(error => console.error('Error reading file:', error));
}

// Watch for changes in convo and scroll to bottom
watch(convo, () => {
    const convoContainer = document.querySelector('.convo');
    convoContainer.scrollTop = convoContainer.scrollHeight;
});

let bot="Vertex AI";
</script>

<template>
    <NavigationBarView2 />
    <div class="home-container">
        <SidePane />
        <div class="main-pane">
            <BreadCrumb :data="bread_path_json" />
            <div class="bot_title">
                <div :class="['who_are_you', { 'con_dis': !connected }]">{{ bot }}</div>
                <div class="who_are_con">
                    <img :src="ChatbotImg" class="who_are" v-if="connected" />
                    <img src="@/assets/dis.png" class="who_are con_dis" v-else="connected" />
                </div>
            </div>
            <div class="convo_cont">
                <div class="convo" id="convo">
                    <div v-for="(convoItem, index) in convo" :key="index" :title="convoItem.recipient">
                        <div class="recip" :class="{ 'recip_me': convoItem.recipient == current_user }">
                            {{ convoItem.recipient }}
                        </div>
                        <div class="class_them_con" :class="{ 'convo_me': convoItem.recipient == current_user }">
                            <div :class="['convo_them', { 'convo_me_msg': convoItem.recipient == current_user }]">
                                <div class="convo_message">{{ convoItem.message }}</div>
                                <div v-if="convoItem.attachments && convoItem.attachments.length">
                                    <div v-for="(attachment, aIndex) in convoItem.attachments" :key="aIndex" class="attachment_item" :title="getFileTitle(attachment)">
                                        <div class="attachment-preview">
                                            <img v-if="attachment.type && attachment.type.includes('image')" :src="attachment.url" class="attachment-img" />
                                            <span v-else class="attachment-icon">📄</span>
                                        </div>
                                        <div class="attachment-info">
                                            <span class="file-name">{{ attachment.name }}</span>
                                            <div class="file-size">({{ (attachment.size / 1024).toFixed(2) }} KB)</div>
                                        </div>
                                    </div>
                                </div>
                                <div v-if="convoItem.attachment && Object.keys(convoItem.attachment).length">
                                    <div v-for="(attachment, aIndex) in convoItem.attachment" :key="aIndex" class="attachment_item" :title="getFileTitle(attachment)">
                                        <div class="attachment-preview">
                                            <img v-if="attachment.mime_type && attachment.mime_type.includes('image')" :src="attachment.path" class="attachment-img" />
                                            <span v-else class="attachment-icon">📄</span>
                                        </div>
                                        <div class="attachment-info">
                                            <span class="file-name">{{ attachment.filename }}</span>
                                            <div class="file-size">({{ (attachment.size / 1024).toFixed(2) }} KB)</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="convo_date">{{ convoItem.time }}</div>
                        </div>
                    </div>
                    <div class="class_them_con" v-if="waiting_for_response">
                        <div class="convo_them">
                            <div class="convo_message convo_loading" style="animation-delay: 0s;"></div>
                            <div class="convo_message convo_loading" style="animation-delay: 0.2s;"></div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="convo_msger" v-if="!closed_chat.ticket_id">
                <div class="input_cmds">
                    <button class="convo_cmd" @click="sendMessage('/create')">/create</button>
                    <button class="convo_cmd" @click="sendMessage('/stop')">/stop</button>
                    <button class="convo_cmd" @click="sendMessage('/status')">/status</button>
                    <button class="convo_cmd" @click="sendMessage('/change')">/change</button>
                    <div class="attachment_list">
                        <!-- {{ attachments }}
                        {{ clipboardAttachments }}
                        {{files}} -->
                        <div v-for="(file, index) in attachments" :key="index" class="attachment_item"
                            :title="getFileTitle(file)">
                            <div class="attachment-preview">
                                <img v-if="file && file.type && file.type.includes('image')" :src="file.url"
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
                <div class="input_cont">
                    <input v-model="messageInput" type="text" class="convo_input" placeholder="Type a message..."
                        @keyup.enter="sendMessage(null)" />
                    <input type="file" multiple ref="fileInput" id="file_input" class="convo_input_file"
                        @change="handleFileInput" style="display: none;" />

                    <button class="convo_send convo_attach" @click="$refs.fileInput.click()">
                        <img src="https://img.icons8.com/?size=100&id=59728&format=png&color=000000"
                            class="attach_img" />
                    </button>

                    <button @click="sendMessage(null)" class="convo_send">Send</button>
                </div>
            </div>
            <div v-else class="closed_chat">
                <!-- go to /ticket/ticket_id -->
                <div class="closed_button" @click="router.push(`/ticket/${closed_chat.ticket_id}`)">
                Chat Closed & Linked with Ticket : {{ closed_chat.ticket_id }}</div>
            </div>
        </div>
    </div>
</template>



<style>
.closed_button{
    background-color: rgba(128, 128, 128, 0.2);
    padding: 0.5vw;
    border-radius: 0.5vw;
    margin-bottom: 0.2vw;
    font-size: 0.8vw;
    font-family: wl1;
    display: flex;
    /* gap: 2vw; */
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: center;
    align-items: center;
    padding: 0.5vw 1.4vw;
    gap: 1.2vw;
    cursor: pointer;
}
.closed_button:hover{
    background-color: rgba(128, 128, 128, 0.3);
    cursor: pointer;
}
.closed_chat{
    margin-top: 2.6vw;
    display: flex;
    width: 100%;
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: center;
    align-items: center;
    gap: 1vw;
    color: rgba(128, 128, 128, 0.35);
    cursor: pointer;
}
.btn_cancel_file {
    padding: 0vw 0vw;
    color: rgba(77, 4, 4, 0.557);
    border: 0.05vw solid rgb(77, 4, 4);
    border-radius: 0.3vw;
    cursor: pointer;
    filter: saturate(0.3);
}

.btn_cancel_file:hover {
    /* background-color: rgb(208, 44, 44); */
    color: white;
    filter: saturate(1);
}

.btn_cancel_file {
    background: none;
    border: none;
    font-size: 0.7vw;
    cursor: pointer;
    padding-left: 0.3vw;
    color: #ff0000;
}

.attachment_item {
    background-color: rgba(128, 128, 128, 0.2);
    padding: 0.5vw;
    border-radius: 0.5vw;
    margin-bottom: 0.2vw;
    font-size: 0.8vw;
    font-family: wl1;
    display: flex;
    /* gap: 2vw; */
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: center;
    align-items: center;
    padding: 0.5vw 1.4vw;
    gap: 1.2vw;
}

.attachment_list {
    position: fixed;
    width: 20vw;
    height: 2vw;
    border-radius: 0.7vw;
    left: 30vw;
    /* background-color: rgba(128, 128, 128, 0.198); */
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: flex-end;
    justify-content: flex-end;
    align-items: stretch;
}

.attachments-list {
    display: flex;
    flex-direction: row;
    max-width: 35vw;
    gap: 2vw;
    row-gap: 1vw;
    flex-wrap: wrap;
    align-content: flex-start;
    justify-content: flex-start;
    align-items: flex-start;
    transform: scale(0.8);
    /* height: 3vw; */
}

.attachment-item {
    flex: 1 1 calc(50% - 2vw);
    box-sizing: border-box;
}

.attachment-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border: 0.1vw solid #ccc;
    border-radius: 0.3vw;
    padding: 0.5vw;
    margin-bottom: 0vw;
    width: 100%;

    max-width: 16vw;
    margin-top: 0vw;

    /* padding: 0vw 1  rem; */
}

.attachment-preview {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2.5vw;
    height: 2.5vw;
    border: 0.1vw solid #ddd;
    border-radius: 0.3vw;
    overflow: hidden;
}

.attachment-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.attachment-icon {
    font-size: 1vw;
    color: #666;
}

.attachment-info {
    flex-grow: 1;
    margin-left: 0vw;
}

.file-name {
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 11vw;
    width: 20vw;
    display: block;
}

.file-size {
    font-size: 0.6vw;
    color: #777;
}

.file-details {
    font-size: 0.6vw;
    color: #555;
    margin-top: 0vw;
}

.convo_loading {
    width: 10vw;
    height: 0.5vw;
    border-radius: 0.5vw;
    margin-bottom: 0.2vw;
    background: linear-gradient(90deg, rgba(128, 128, 128, 0.1), rgba(128, 128, 128, 0.3), rgba(128, 128, 128, 0.1));
    background-size: 200% 100%;
    animation: convo_loading 1s infinite;
}

@keyframes convo_loading {
    0% {
        background-color: rgba(128, 128, 128, 0.3);
    }

    50% {
        background-color: rgba(128, 128, 128, 0.0);
    }

    100% {
        background-color: rgba(128, 128, 128, 0.3);
    }
}

.input_cmds {
    display: flex;
    flex-direction: row;
    gap: 0.5vw;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: flex-end;
    align-items: center;
    margin-top: 1vw;
    width: 89%;
}

.convo_cmd {
    border-radius: 2vw;
    border: 0.1vw solid rgba(128, 128, 128, 0);
    padding: 0.4vw;
    /* margin-left: 1vw; */
    background-color: rgba(128, 128, 128, 0.08);
    color: black;
    cursor: pointer;
    width: 7vw;
    text-align: center;
    font-family: wl1;
    font-size: 0.8vw;
}

.convo_cmd:hover {
    background-color: rgba(128, 128, 128, 0.241);
}

.convo_send {
    border-radius: 0.5vw;
    border: 0.1vw solid grey;
    padding: 0.7vw;
    font-size: 0.9vw;
    margin-left: 1vw;
    background-color: grey;
    color: white;
    cursor: pointer;
    width: 7vw;
    text-align: center;
    font-family: wl1;
    height: 3vw;
    width: 5vw;
    margin-right: 2vw;
}

.convo_send:hover {
    background-color: rgb(0, 92, 92);
}

.convo_input {
    height: 2vw;
    border-radius: 0.5vw;
    /* border: 0.1vw solid grey; */
    border: none;
    background-color: rgba(128, 128, 128, 0.1);
    padding: 0.5vw 1vw;
    font-size: 0.8vw;
    width: 49vw;
    font-family: wl1;
    border: 0.1vw solid rgba(0, 128, 128, 0);
}

.convo_input:hover {
    background-color: rgba(128, 128, 128, 0.15);
}

.convo_input:focus {
    outline: none;
    border: 0.1vw solid teal;
}

.input_cont {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: center;
    align-items: center;
    color: grey;
    margin-top: 1vw;
}

.convo_msger {
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: center;
    align-items: center;
    gap: 0vw;
    margin: 2vw 5vw;
    width: 67vw;
    position: fixed;
    bottom: 0;
    /* background-color: rgb(225, 225, 225); */
}

.recip_me {
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-items: flex-end;
}

.recip {
    font-size: 0.9vw;
    margin-bottom: 0.2vw;
    /* text-transform: capitalize; */
}

.convo_date {
    font-size: 0.5vw;
    margin-top: 0.3vw;
}

.class_them_con {
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: center;
    align-items: flex-start;
}

.convo_them:hover {
    background-color: rgba(128, 128, 128, 0.241);
    cursor: pointer;
}

.convo_cont {
    width: 86%;
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: center;
    margin: 2vw 4vw;
    margin-top: 0vw;
    align-items: center;
    /* height: 33vw; */
    overflow-y: auto;
}

.convo_message {
    font-size: 0.8vw;
    max-width: 40vw;
}

.convo {
    width: 90%;
    padding: 2vw;
    padding-top: 0vw;
    /* background-color: rgba(213, 213, 213, 0.064); */
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: flex-start;
    justify-content: flex-start;
    /* gap: 1vw; */
    height: 50vh;
    overflow-y: scroll;
    scroll-behavior: smooth;

}

.convo::-webkit-scrollbar {
    width: 0.4vw;
    height: 0.5vw;
    cursor: pointer;
    opacity: 0;
}

.convo:hover::-webkit-scrollbar {
    opacity: 1;
}

.convo::-webkit-scrollbar-thumb {
    background-color: #c8c8c8;
    border-radius: 0.3vw;
}

.convo::-webkit-scrollbar-track {
    background-color: #f0f0f0;
}

.convo_them {
    background-color: rgba(225, 225, 225, 0.809);
    padding: 1vw;
    border-radius: 0.6vw;
    width: fit-content;
    font-size: 0.9vw;
    border-bottom-left-radius: 0;
    font-size: 0.7vw;
    font-family: wl1;
}

.convo_them {
    background-color: rgba(218, 241, 251, 0.809);

}

.convo_me_msg {
    background-color: rgba(218, 251, 227, 0.809);
    border-bottom-left-radius: 0.6vw;
    border-bottom-right-radius: 0;
}

.bot_title {
    display: flex;
    flex-direction: row;
    gap: 1.5vw;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: center;
    align-items: center;
    margin-top: 1vw;
    padding-bottom: 2vw
}

.who_are_you {
    background-color: rgba(128, 128, 128, 0.1);
    width: 10vw;
    height: 3vw;
    border-radius: 0.5rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-items: center;
    justify-content: center;
    align-content: center;
    flex-wrap: nowrap;
    margin-left: 5vw;
    cursor: pointer;
    border-radius: 5vw;
    font-family: wl3;
    color: teal;
}

.bot_title:hover {
    cursor: pointer;
}

.bot_title:hover .who_are_you {
    background-color: rgba(128, 128, 128, 0.3);
}

.bot_title:hover .who_are_con {
    border: 0.1vw black solid;
}

.who_are_con {
    width: 2.5vw;
    height: 2.5vw;
    border: 0.1vw solid grey;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-items: center;
    justify-content: center;
    align-content: center;
    flex-wrap: nowrap;
    border-radius: 50%;
}

.who_are {
    padding: 0.1rem;
    border-radius: 50%;
    width: 2vw;
    height: 2vw;
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
}

.main-pane {
    display: flex;
    align-items: flex-start;
    flex-direction: column;
    width: 100%;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: flex-start;
}

.home-container {
    justify-content: flex-start;
    display: flex;
    flex-direction: row;
    overflow: hidden;
    height: fill-available;
    height: 90vh;


}

.tile-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    overflow-x: hidden;
    overflow-y: auto;
    margin-left: 4rem;
}

.convo_me {
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: center;
    align-items: flex-end;
}

.convo_attach {
    height: 3vw;
    width: 3vw;
    background-color: grey;
    margin-right: 0;

}

.convo_attach img {
    height: 1.5vw;
    width: 1.5vw;
    filter: invert(1);
}

.convo_connect {
    width: 1vw;
    height: 1vw;
    background-color: grey;
    margin-right: 0;
    border-radius: 50%;
}

.con_dis {
    color: rgb(126, 13, 13);
}
</style>
