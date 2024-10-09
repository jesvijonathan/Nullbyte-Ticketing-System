<template>
  <div class="sidepane-item">
    <div v-if="!isExpanded" class="ticket">{{ ticket.TicketNo }} : {{ ticket.TicketName }}</div>
    <div v-if="isExpanded" class="ticket-details">
      <div class="detail"><span>{{ ticket.TicketNo }} : {{ ticket.TicketName }}</span></div>
      <div class="detail">
        <span class="label">Date</span>
        <span class="colon">|</span>
        <span class="value">{{ ticket.Date }}</span>
      </div>
      <div class="detail">
        <span class="label">Created By</span>
        <span class="colon">|</span>
        <span class="value">{{ ticket['Created By'] }}</span>
      </div>
      <div class="detail">
        <span class="label">Assigned To</span>
        <span class="colon">|</span>
        <span class="value">{{ ticket['Assigned To'] }}</span>
      </div>
      <div class="detail">
        <span class="label">Status</span>
        <span class="colon">|</span>
        <span class="value">{{ ticket.Status }}</span>
      </div>
      <div class="detail">
        <span class="label">Issue Type</span>
        <span class="colon">|</span>
        <span class="value">{{ ticket['Issue Type'] }}</span>
      </div>
      <div class="detail">
        <span class="label">Team</span>
        <span class="colon">|</span>
        <span class="value">{{ ticket.Team }}</span>
      </div>
    </div>
    <img :src="angledown" class="ico" v-if="!isExpanded" alt="angledown" @click.stop="toggleExpand"/>
    <img :src="angledown" class="ico" v-if="isExpanded" alt="angledown" @click.stop="toggleExpand" style="transform: rotate(180deg);"/>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import angledown from '@/assets/angle-down-solid.svg';

export default defineComponent({
  name: 'SidePaneItem',
  props: {
    ticket: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      angledown,
      isExpanded: false
    };
  },
  methods: {
    toggleExpand() {
      this.isExpanded = !this.isExpanded;
    }
  }
});
</script>

<style scoped>
* {
  color: white;
  box-sizing: border-box;
}
.sidepane-item {
  margin: 10px 5px;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s;
  border: 1px solid white; 
  border-radius: 4px;
  background: rgb(0, 0, 0);
  background: linear-gradient(90deg, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 1) 97%, rgb(199, 199, 199) 100%);
  display: flex;
  flex-direction: row;
  transform: ease-in-out;
  transition: 0.3s;
  justify-content: space-between;
}

.sidepane-item:hover {
  background: linear-gradient(90deg, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 1) 97%, #46BEAA 100%);
}

.ticket {
  color: white;
  font-size: 12px;
  display: flex;
  flex-direction: column;
}

.ticket-details {
  width: 100%;
}

.detail {
  display: flex;
  align-items: center;
  justify-content: space-between; 
  font-size: 11px;
  color: white;
}

.label {
  flex: 1; 
  text-align: left; 
}

.colon {
  flex: 0 0 10px; 
  text-align: center; 
  color: #79797971;
}

.value {
  flex: 2;
  text-align: right;
}
.ico {
  align-self: flex-end;
  margin-left: 4px;
  margin-right: 0px;
}
</style>
