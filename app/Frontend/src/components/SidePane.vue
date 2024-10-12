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
        <div class="create_con" v-if="$route.path === '/dashboard'">
          <div  
            @click="handleClick()" 
            :key="CreateTicket" 
            class="side-pane-title-elements">
            Create Ticket
          </div>
          <hr style="
    margin-bottom: 1rem; width: 14rem;border: 0.08rem solid #818181;">
          </div>
          <SidePaneItem class="side_panel_item" v-for="ticket in TicketItems" :key="ticket.TicketNo" :ticket="ticket"/>
        
      </div>
      <div class="sp-footer"><div class="powered-by">Powered By </div><h1 class="nulllfont">Nullbyte</h1></div>
    </div>
  </template>
  
  <style scoped>
  .create_con{
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: center;
    align-items: center;
  }
.powered-by{
  font-family: 'wl1';
  font-size: 1rem;
}
.sp{    
  height: 82vh;
  overflow: overlay;    
  padding-right: 2.4rem;

}

  .sp-footer{
    display: flex;
    justify-content: center;
    align-items: center;
    color: #46BEAA;
    gap: 0.55rem;    
    transform: scale(1);  
    cursor: pointer;
    padding-right: 2.4rem;
  }
  .sp-footer:hover .nulllfont{
    transform: skew(-17deg);
  }
  .sp-footer *{
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
    width: 50rem;
    /* height: 100%; */
    /* overflow: hidden; */
    background-color: #272727;
    border-right: 1px solid #dee2e6;
    padding: 1rem 2.4rem;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
    /* overflow-y: auto; */
    flex-wrap: nowrap;
    height: fill-available;
    /* width: 17rem; */    
    padding: 1rem 0rem 1rem 2.4rem;
    overflow-x: inherit;
  }
  
  .side-pane-title-elements {
    color: white;
    padding: 10px;
    border: 1px solid white;
    justify-content: center;
    align-items: center;
    display: flex;
    border-radius: 10px;
    margin: 1.3rem 2rem 2rem 2rem;
    cursor: pointer;
    width: 15rem;
  }
  
  .side-pane-title-elements:hover {
    border: 1px solid #46BEAA;
    background-color: #46BEAA;
  }
  

  /* slim scroll bar for   .side-pane */
.sp::-webkit-scrollbar {
  width: 0.4rem;
}
.sp::-webkit-scrollbar-thumb {
  background-color: #4a4a4a;
  border-radius: 1rem;
}
.sp::-webkit-scrollbar-thumb:hover {
  background-color: #818181;
}
.sp::-webkit-scrollbar-track {
  background-color: #272727;
}




  </style>
  