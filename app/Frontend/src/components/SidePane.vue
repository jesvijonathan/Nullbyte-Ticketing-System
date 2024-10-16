<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import SidePaneItem from './SidePaneItem.vue';

const sidePaneItems = ['Dashboard', 'Chatbot', 'Inbox', 'Ticket', 'Reports', 'HelpDesk', 'Create Ticket'];

const TicketItems = ref([
  {
    chat_id: "tRAFcELKK5xiAK6FAAAD",
    ticket_id: "SVC-000000",
    user: "admin",
    medium: "",
    connection: "closed",
    text: "wlpfo is declining transactions where the P025 field is set to 28, while transactions with P025 value 00 are being approved. The logs indicate an issue within the transaction processing logic related to the P025 field. Clarification is required for the correct values for P025.",
    subject: "wlpfo Transaction Declined for P025 Value 28",
    summary: "wlpfo is declining transactions where the P025 field is set to 28, while transactions with P025 value 00 are being approved. The logs indicate an issue within the transaction processing logic related to the P025 field. Clarification is required for the correct values for P025.",
    attachments: [
      {
        name: "Transaction Logs",
        type: "text/plain",
        url: "https://example.com/logs.txt",
        details: "The logs show successful transactions when P025 is 00 and declined transactions when P025 is 28. Errors like \"[ERROR]: P025 invalid\" are present. The logs also contain details of GICC capture, GICC authorization request, compose message, and e-commerce transaction details. Further analysis suggests potential conflicts with specific transaction parameters or conditions related to P025 field validation.",
        size: "4382"
      }
    ],
    product_type: "wlpfo",
    issue_type: "bug",
    priority: "high",
    story_points: "5",
    estimation: "8",
    analysis: "The issue likely stems from incorrect validation rules or logic for the P025 field within wlpfo. A code review and debugging of the transaction processing module, focusing on P025 handling, are recommended. Testing with various P025 values and different transaction scenarios will help isolate the problem. A potential workaround could involve temporarily disabling the specific P025 validation rule, if feasible, until a permanent fix is implemented.",
    reply: "A ticket has been created to investigate the issue with wlpfo declining transactions for P025 value 28. We will analyze the provided logs and investigate the root cause of the problem. We'll keep you updated on the progress and provide a solution as soon as possible.",
    assingee: "developer_1",
    status: "open",
    created: "2021-07-15T10:00:00",
    updated: "2021-07-15T10:00:00",
    comments: [
      {
        comment_id: "1",
        user: "developer_1",
        text: "I will start investigating the issue with P025 validation in wlpfo. I'll update you with my findings and progress.",
        date: "2021-07-15T10:30:00"
      }
    ],
    logged_hrs: [
      {
        user: "developer_1",
        logged: "2",
        date: "2021-07-15T10:30:00"
      },
      {
        user: "developer_1",
        logged: "3",
        date: "2021-07-16T10:30:00"
      }
    ]
  },
  {
    chat_id: "tRAFcELKK5xiAK6FAAAD",
    ticket_id: "SVC-11111",
    user: "admin",
    medium: "",
    connection: "closed",
    text: "wlpfo is declining transactions where the P025 field is set to 28, while transactions with P025 value 00 are being approved. The logs indicate an issue within the transaction processing logic related to the P025 field. Clarification is required for the correct values for P025.",
    subject: "wlpfo Transaction Declined for P025 Value 28",
    summary: "wlpfo is declining transactions where the P025 field is set to 28, while transactions with P025 value 00 are being approved. The logs indicate an issue within the transaction processing logic related to the P025 field. Clarification is required for the correct values for P025.",
    attachments: [
      {
        name: "Transaction Logs",
        type: "text/plain",
        url: "https://example.com/logs.txt",
        details: "The logs show successful transactions when P025 is 00 and declined transactions when P025 is 28. Errors like \"[ERROR]: P025 invalid\" are present. The logs also contain details of GICC capture, GICC authorization request, compose message, and e-commerce transaction details. Further analysis suggests potential conflicts with specific transaction parameters or conditions related to P025 field validation.",
        size: "4382"
      }
    ],
    product_type: "wlpfo",
    issue_type: "bug",
    priority: "high",
    story_points: "5",
    estimation: "8",
    analysis: "The issue likely stems from incorrect validation rules or logic for the P025 field within wlpfo. A code review and debugging of the transaction processing module, focusing on P025 handling, are recommended. Testing with various P025 values and different transaction scenarios will help isolate the problem. A potential workaround could involve temporarily disabling the specific P025 validation rule, if feasible, until a permanent fix is implemented.",
    reply: "A ticket has been created to investigate the issue with wlpfo declining transactions for P025 value 28. We will analyze the provided logs and investigate the root cause of the problem. We'll keep you updated on the progress and provide a solution as soon as possible.",
    assingee: "developer_1",
    status: "open",
    created: "2021-07-15T10:00:00",
    updated: "2021-07-15T10:00:00",
    comments: [
      {
        comment_id: "1",
        user: "developer_1",
        text: "I will start investigating the issue with P025 validation in wlpfo. I'll update you with my findings and progress.",
        date: "2021-07-15T10:30:00"
      }
    ],
    logged_hrs: [
      {
        user: "developer_1",
        logged: "2",
        date: "2021-07-15T10:30:00"
      },
      {
        user: "developer_1",
        logged: "3",
        date: "2021-07-16T10:30:00"
      }
    ]
  }
]);

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

    </div>
    <div class="sp-footer">
      <div class="powered-by">Powered By </div>
      <h1 class="nulllfont">Nullbyte</h1>
    </div>
  </div>
</template>

<style scoped>
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