<template>
  <div
    class="sidepane-item"
    :style="[getBorderColor(ticket.Status), isHovered ? getHoverBorderColor(ticket.Status) : {}]"
    @mouseover="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <div v-if="!isExpanded" class="ticket">{{ ticket.TicketNo }} : {{ ticket.TicketName }}</div>
    <div v-if="isExpanded" class="ticket-details">
      <div class="detail"><span class="ticket_name_det">{{ ticket.TicketNo }} : {{ ticket.TicketName }}</span></div>
      <hr class="splitter" />
      <div class="detail">
        <span class="label">Date</span>
        <span class="colon">:</span>
        <span class="value">{{ ticket.Date }}</span>
      </div>
      <div class="detail">
        <span class="label">Created By</span>
        <span class="colon">:</span>
        <span class="value">{{ ticket['Created By'] }}</span>
      </div>
      <div class="detail">
        <span class="label">Assigned To</span>
        <span class="colon">:</span>
        <span class="value">{{ ticket['Assigned To'] }}</span>
      </div>
      <div class="detail">
        <span class="label">Status</span>
        <span class="colon">:</span>
        <span class="value">{{ ticket.Status }}</span>
      </div>
      <div class="detail">
        <span class="label">Issue Type</span>
        <span class="colon">:</span>
        <span class="value">{{ ticket['Issue Type'] }}</span>
      </div>
      <div class="detail">
        <span class="label">Team</span>
        <span class="colon">:</span>
        <span class="value">{{ ticket.Team }}</span>
      </div>
    </div>
    <img :src="angledown" :class="isExpanded ? 'ico_rot' : 'ico'" alt="angledown" @click.stop="toggleExpand" />
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
      isExpanded: false,
      isHovered: false // To track hover state
    };
  },
  methods: {
    toggleExpand() {
      this.isExpanded = !this.isExpanded;
    },
    getBorderColor(status) {
      if (status.toLowerCase() === 'open') {
        return { borderRight: '0.33rem solid grey' }; // Grey for open status
      } else if (status.toLowerCase() === 'closed') {
        return { borderRight: '0.33rem solid #46BEAA' }; // Green for closed status
      } else {
        return { borderRight: '0.33rem solid #8B3939' }; // Red for any other status
      }
    },
    getHoverBorderColor(status) {
      if (status.toLowerCase() === 'open') {
        return { borderRight: '0.33rem solid #b3b3b3' }; // Brighter grey for hover
      } else if (status.toLowerCase() === 'closed') {
        return { borderRight: '0.33rem solid #00FFE3' }; // Brighter green for hover
      } else {
        return { borderRight: '0.33rem solid #FF0303' }; // Brighter red for hover
      }
    }
  }
});
</script>

<style scoped>
* {
  color: white;
  box-sizing: border-box;
}

.splitter {
  margin: 0.4rem 0rem 1rem 0rem;
  border: 0.1rem solid #79797971;
}

.ticket_name_det {
  /* text-align: center;
  width: 100%; */
  font-size: 0.7rem;
  width: 13.5rem;
  text-transform: uppercase;
  overflow: clip;
}

.sidepane-item {
  margin: 1em 0rem;
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.7);
  border-radius: 0.4rem;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center; /* Align items to ensure text stays on one line */
  width: 100%;
  overflow: hidden; /* Ensures the container doesn't expand beyond its width */
  text-overflow: ellipsis;
  border-right: 0.33rem solid #c7c7c7ab;
  padding: 0.8rem 0rem 0.8rem 1rem;
  transition: 0s;
}


.sidepane-item:hover{
  background-color: #4646463f;
}


.ticket {
  color: white;
  font-size: 0.7rem;
  display: flex;
  flex-direction: column;
  text-transform: uppercase;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden; /* Clips the text if it overflows */
  width: 100%; /* Ensures the ticket content occupies full width */
  margin-right: 0.7rem;
}

.ticket-details {
  width: 100%;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: flex;
  flex-direction: column;
  align-content: center;
  justify-content: center;
  align-items: stretch;
  flex-wrap: nowrap;
  width: 15rem;
  font-size: 0.6rem;
}

.detail {
  display: flex;
    align-items: baseline;
    justify-content: flex-start;
    color: white;
    max-width: 17rem;
    flex-direction: row;
    flex-wrap: nowrap;

}

.label {
  flex: 1;
  text-align: left;
  text-transform: uppercase;
}

.colon {
  flex: 0 0 10px;
  text-align: center;
  color: #79797971;
}

.value {
  flex: 2;
  /* text-align: right; */
  color: rgba(255, 255, 255, 0.775);
  font-weight: 100;
}

.ico {
  align-self: flex-end;
  height: 1rem;
  padding: 0rem 1rem 0rem 0.3rem;
  transition: 0s ease-in-out;
  opacity: 0.6;
}

.ico_rot {
  align-self: flex-end;
  height: 1rem;
  padding: 0rem 0.3rem 0rem 1rem;
  transform: rotate(-180deg);
  transition: 0s ease-in-out;
  opacity: 0.6;
}

.ico:hover,
.ico_rot:hover {
  cursor: pointer;
  opacity: 1;
}
</style>
