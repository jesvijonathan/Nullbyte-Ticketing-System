<script>
import SidePaneItem from './SidePaneItem.vue';

export default {
  name: 'Sidepane',
  components:{
    SidePaneItem
  },
  data() {
    return {
      sidePaneItems: ['Dashboard', 'Chatbot', 'Inbox', 'Ticket', 'Reports', 'HelpDesk', 'Create Ticket'],
      TicketItems: [
        {
          'TicketNo': 'SVC-42069',
          'TicketName': 'Eat 5 Star Do nothing and get paid',
          'Date': '12/12/2021',
          'Created By': 'John Doe',
          'Assigned To': 'Jane Doe',
          'Status': 'Open',
          'Issue Type': 'Bug',
          'Team': 'Development'
        },
        {
          'TicketNo': 'SVC-42070',
          'TicketName': 'Fix login issue',
          'Date': '13/12/2021',
          'Created By': 'Alice Smith',
          'Assigned To': 'Bob Johnson',
          'Status': 'In Progress',
          'Issue Type': 'Bug',
          'Team': 'QA'
        },
        {
          'TicketNo': 'SVC-42071',
          'TicketName': 'Update user profile page',
          'Date': '14/12/2021',
          'Created By': 'Charlie Brown',
          'Assigned To': 'David Wilson',
          'Status': 'Closed',
          'Issue Type': 'Enhancement',
          'Team': 'UI/UX'
        },
        {
          'TicketNo': 'SVC-42072',
          'TicketName': 'Database optimization',
          'Date': '15/12/2021',
          'Created By': 'Eve Davis',
          'Assigned To': 'Frank Miller',
          'Status': 'Open',
          'Issue Type': 'Performance',
          'Team': 'Backend'
        }
      ]
    };
  },
  methods: {
    handleClick() {
      alert(`Comming Soon!`);
    }
  }
};
</script>

<template>
    <div class="side-pane">
      <div class="sp">
        <!-- Iterate over sidePaneItems and call handleClick on click -->
        <div v-if="$route.path === '/service'">
          <div 
            v-for="item in sidePaneItems" 
            @click="handleClick()" 
            :key="item" 
            class="side-pane-title-elements">
            {{ item }}
          </div>
        </div>
        <div v-if="$route.path === '/dashboard'">
          <div  
            @click="handleClick()" 
            :key="CreateTicket" 
            class="side-pane-title-elements">
            Create Ticket
          </div>
          <hr>
          <SidePaneItem v-for="ticket in TicketItems" :key="ticket.TicketNo" :ticket="ticket"/>
        </div>
      </div>
      <div class="sp-footer">Powered By NULLBYTE</div>
    </div>
  </template>
  
  <style scoped>
  .side-pane {
    /* position:fixed; */
    display: flex;
    /* overflow: hidden; */
    left:0;
    flex-direction: column;
    justify-content: space-between;
    width: 45%;
    min-height: 100vh;
    overflow: hidden;
    background-color: #000000;
    border-right: 1px solid #dee2e6;
    padding: 20px;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
    /* overflow-y: auto; */

  }
  
  .side-pane-title-elements {
    color: white;
    padding: 10px;
    border: 1px solid white;
    justify-content: center;
    align-items: center;
    display: flex;
    border-radius: 10px;
    margin: 20px;
  }
  
  .side-pane-title-elements:hover {
    color: black;
    border: 1px solid black;
    background-color: #46BEAA;
    transform: scale(1.1);
  }
  
  .sp-footer {
    color: #46BEAA;
    display: flex;
    justify-content: center;
  }
  </style>
  