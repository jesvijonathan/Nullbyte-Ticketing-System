<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import SidePaneItem from './SidePaneItem.vue';

const sidePaneItems = ['Dashboard', 'Chatbot', 'Inbox', 'Ticket', 'Reports', 'HelpDesk', 'Create Ticket'];

const TicketItems = ref([
]);


let get_tickets =''
if(document.useDB)
get_tickets= document.baseMyURL+"/ticket/get";
else
get_tickets= document.baseMyURL+"/get_tickets";

onMounted(async () => {

  const response = await fetch(get_tickets);
        const data = await response.json();
        Object.keys(data).forEach(ticket_id => {
            const ticket_info = data[ticket_id];
            const tmp_tick = ticket_info.closed_chat || ticket_info;
            console.log("jesvi ::::", tmp_tick)
            TicketItems.value.push(tmp_tick);
        });

      console.log("#####jesvi :", TicketItems.value)


      if (router.currentRoute.value.path.includes('chatbot') || router.currentRoute.value.path.includes('vertex') || router.currentRoute.value.path.includes('llama')) {
  const userId = cookies.get('user');  // Get the user ID from cookies

  if (userId) {
    try {
      const response = await fetch(chat_data_url + '/' + userId);  // Use a standard CORS request

      if (!response.ok) {
        console.error('Error fetching chat data:', response.statusText);
        return;  // Stop execution if the response is not okay
      }

      const data = await response.json();  // Parse the JSON response
      console.log('Chat data:', data);

      // Update the chat_data reactive variable
      for (const key in data["chat_history"]) {
        chat_data.value[key] = data["chat_history"][key];
      }
      console.log('Updated chat data:', chat_data.value);

    } catch (error) {
      console.error('Fetch error:', error);  // Catch any fetch or network errors
    }
  } else {
    console.error('User ID not found in cookies.');
  }
}

});

const router = useRouter();

const handleClick = (url) => {
  router.push(url);
};

let mini=ref(false);


function minimize() {
  if (mini.value) {
    var minimize = document.getElementById('minimize');
    minimize.style.transform = 'translate(0%, -50%) rotate(90deg) scale(1.6)';
    minimize.style.left = '23vw';
    mini.value = !mini.value;
    return;
  }else{
  var minimize = document.getElementById('minimize');
  minimize.style.transform = 'translate(0%, -50%) rotate(270deg) scale(1.6)';  
  minimize.style.left = '1vw';
  mini.value = !mini.value;}
}



const show_extra_dashboard = ref(false);

const chat_data_url = document.baseMyURL + "/get_chat_history";

import { useCookies } from 'vue3-cookies';

const current_user = ref(null);
const { cookies } = useCookies();

const chat_data = ref({});


function handleClick_new(chat_id) {

}
 



</script>


<template>
  <div class="minimize" @click="minimize()" id="minimize">
    <img src="@/assets/angle-down-solid.svg" alt="angle-down-solid" />
  </div>
  <div class="side-pane" id="side-pane" v-if="!mini">
    <div class="sp">
      <!-- Iterate over sidePaneItems and call handleClick on click -->
      <div v-if="$route.path === '/service'">
        <div v-for="item in sidePaneItems" @click="handleClick()" :key="item" class="side-pane-title-elements">
          {{ item }}
        </div>
      </div>
      <div class="create_con" v-if="$route.path === '/dashboard'">
        <div @click="handleClick('/create_ticket')" :key="CreateTicket" class="side-pane-title-elements first_nike">
          Create Ticket
        </div>
        <hv class="hv"></hv>
        <div @click="handleClick('/list_tickets')" :key="CreateTicket" class="side-pane-title-elements nike" v-if="show_extra_dashboard">
          All Tickets
        </div>
        <div @click="handleClick('/list_tickets')" :key="CreateTicket" class="side-pane-title-elements nike" v-if="show_extra_dashboard">
          Action Items
        </div>
        <div @click="handleClick('/list_tickets')" :key="CreateTicket" class="side-pane-title-elements nike" v-if="show_extra_dashboard">
          Unassigned Tickets
        </div>
        <hr class="hv" v-if="show_extra_dashboard">

        <div @click="handleClick('/text')" :key="CreateTicket" class="side-pane-title-elements nike" v-if="show_extra_dashboard">
          Chatbot
        </div>
        <div @click="handleClick('/profile')" :key="CreateTicket" class="side-pane-title-elements nike" v-if="show_extra_dashboard">
          Settings
        </div>
        <hr class="hv" v-if="show_extra_dashboard">

      </div>

      <div class="create_con tpls" v-if="$route.path.includes('ticket')">
        <div @click="handleClick('/list_tickets')" :key="CreateTicket" class="side-pane-title-elements tpl tp1">
          All Ticket
        </div>
        <div @click="handleClick('/create_ticket')" :key="CreateTicket" class="side-pane-title-elements tpl">
          New Ticket
        </div>
        <div @click="handleClick('/list_tickets?category=my_tickets')" :key="CreateTicket" class="side-pane-title-elements tpl  ">
          My Tickets
        </div>
        <div @click="handleClick('/list_tickets?category=pending')" :key="CreateTicket" class="side-pane-title-elements tpl">
          Action Items
        </div>
        <div @click="handleClick('/list_tickets')" :key="CreateTicket" class="side-pane-title-elements tpl">
          Unassigned Tickets
        </div>

        <hr class="hv" v-if="$route.path.includes('ticket') && $route.path != '/list_tickets'">
      </div>


      <div class="create_con tpls" v-if="$route.path.includes('profile')">
        <div @click="handleClick('/profile')" :key="CreateTicket" class="side-pane-title-elements tpl tp1">
          My Profile
        </div>
        <div @click="handleClick('/profile')" :key="CreateTicket" class="side-pane-title-elements tpl">
          Account
        </div>
        <div @click="handleClick('/profile')" :key="CreateTicket" class="side-pane-title-elements tpl  ">
          Notifications
        </div>
        <div @click="handleClick('/profile')" :key="CreateTicket" class="side-pane-title-elements tpl">
          Security
        </div>
        <div @click="handleClick('/logout')" :key="CreateTicket" class="side-pane-title-elements tpl">
          Logout
        </div>

        <hr class="hv" v-if="$route.path.includes('ticket') && $route.path != '/list_tickets'">
      </div>
      <SidePaneItem class="side_panel_item" v-for="ticket in TicketItems" :key="ticket.ticket_id" :ticket="ticket"
        v-if="$route.path != '/list_tickets' && $route.path != '/profile' && $route.path != '/service' && $route.path != '/chatbot'
         && $route.path != '/llama'  && $route.path != '/vertex' && $route.path != '/about' && $route.path != '/vertex' && $route.path != '/inbox'"
         > </SidePaneItem>

        <div v-if="$route.path.includes('chatbot') || $route.path.includes('vertex') || $route.path.includes('llama')" class="chathist">
          <!-- {{chat_data}} -->
           - Chat History -
           <br><br>
          <!-- @click="handleClick('/ticket/'+item.closed_chat.ticket_id)"> -->
           <div v-for="item in chat_data" :key="item" class="chat_panel"
           @click="handleClick_new(item.closed_chat.chat_id)">
                {{ item.closed_chat.ticket_id }} : {{ item.closed_chat.subjecty ? item.closed_chat.subjecty : "" }}
          </div>
        </div>

    </div>
    <div class="sp-footer">
      <div class="powered-by">Powered By </div>
      <h1 class="nulllfont">Nullbyte</h1>
    </div>
  </div>
</template>

<style scoped>
.chathist{
  margin-top: 1vw;
  margin-bottom: 1vw;
  width: 16vw;
  padding: 0.5vw;
  border-radius: 0.3vw;
  text-align: center;
  cursor: pointer;
  color: white;
}
.chat_panel{
  margin-top: 1vw;
  margin-bottom: 1vw;
  width: 14vw;
  border: 0.08vw solid #818181;
  padding: 0.5vw;
  border-radius: 0.3vw;
  background-color: rgba(255, 255, 255, 0.568);
  text-align: center;
  cursor: pointer;
  font-size: 0.8vw;
  color: rgb(0, 0, 0);
}
.chat_panel:hover{
  background-color: rgba(255, 255, 255, 1);
}
.minimize{
  position: absolute;
  padding: 0.5vw;
  cursor: pointer;
  /* border: 0.2vw red solid; */
  transform: translate(-50%, -50%) rotate(90deg) scale(1.6);
  /* border-radius: 50%; */
  top: 97%;
  left: 24vw;
  z-index: 100;
  filter: invert(1);
  opacity: 0.2;
  top: 95vh;
}
.minimize:hover{
  transform: translate(-50%, -50%) rotate(90deg) scale(1.8);
  opacity: 1;
}
.tpls {
  margin-bottom: 1vw;
}

.create_con {
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  align-content: center;
  justify-content: center;
  align-items: center;
}

.powered-by {
  font-family: 'wl1';
  font-size: 1vw;
}

.sp {
  height: 82vh;
  overflow: overlay;
  padding-right: 2.4vw;

}

.sp-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  color: #46BEAA;
  gap: 0.55vw;
  transform: scale(1);
  cursor: pointer;
  padding-right: 2.4vw;
}

.sp-footer:hover .nulllfont {
  transform: skew(-17deg);
}

.sp-footer * {
  color: #46BEAA;
  display: flex;
  justify-content: center;
}

.side-pane {
  display: flex;
  /* overflow: hidden; */
  left: 0;
  flex-direction: column;
  justify-content: space-between;
  width: 20vw;
  min-width: 20vw;
  /* height: 100%; */
  /* overflow: hidden; */
  background-color: #272727;
  border-right: 0.1vw solid #dee2e6;
  padding: 1vw 2.4vw;
  box-shadow: 0.1vw 0 0.2vw rgba(0, 0, 0, 0.1);
  /* overflow-y: auto; */
  flex-wrap: nowrap;
  height: fill-available;
  /* width: 17vw; */
  padding: 1vw 0vw 1vw 2.4vw;
  overflow-x: inherit;
}

.side-pane-title-elements {
  color: white;
  padding: 0.5vw;
  border: 0.1vw solid white;
  justify-content: center;
  align-items: center;
  display: flex;
  border-radius: 0.4vw;
  margin: 1.3vw 2vw 2vw 2vw;
  cursor: pointer;
  width: 15vw;
  font-size: 0.9vw;
}

.side-pane-title-elements:hover {
  border: 0.1vw solid #46BEAA;
  background-color: #46BEAA;
}

.tpl {
  margin-top: 0.6vw;
  margin-bottom: 0.6vw;
}


/* slim scroll bar for   .side-pane */
.sp::-webkit-scrollbar {
  width: 0.4vw;
}

.sp::-webkit-scrollbar-thumb {
  background-color: #4a4a4a;
  border-radius: 1vw;
}

.sp::-webkit-scrollbar-thumb:hover {
  background-color: #818181;
}

.sp::-webkit-scrollbar-track {
  background-color: #272727;
}

.tplast {
  margin-bottom: 2vw;
}
.tp1{
  margin-top: 2vw;
}

.nike {
  margin-top: 0vw;

  margin: 1vw 2vw 0vw 2vw;
}

.hv {

  margin-bottom: 1vw;
  margin-top: 2vw;
  width: 14vw;
  border: 0.08vw solid #818181;
}
.first_nike{
  margin-bottom: 0vw
}
</style>