<script setup>
import { useAuthStore } from '@/stores/auth';
import Tile from '@/components/Tile.vue';
import SidePane from '@/components/SidePane.vue';
import router  from '../router/';
import BreadCrumb from '@/components/BreadCrumb.vue';
import NavigationBarView from '@/views/NavigationBarView.vue' 
import NavigationBarView2 from '@/views/NavigationBarView_2.vue' 


const authStore = useAuthStore();

import CreateTicketImg from '@/assets/createTicket.svg';
import TicketImg from '@/assets/Ticket.png';
import InboxImg from '@/assets/Inbox.png';
import ChatbotImg from '@/assets/chatbot.svg';
import ReportImg from '@/assets/Report.png';
import AlertImg from '@/assets/Alert.png';
import HelpDeskImg from '@/assets/Service.png';
import ProfileImg from '@/assets/Profile.png';
import AboutImg from '@/assets/About.png';



const tiles = [
    { title: 'Create Tickets', image: CreateTicketImg },
    { title: 'Ticket', image: TicketImg },
    { title: 'Inbox', image: InboxImg },
    { title: 'Chatbot', image: ChatbotImg },
    { title: 'Report', image: ReportImg },
    { title: 'Alert', image: AlertImg },
    { title: 'Help Desk', image: HelpDeskImg },
    { title: 'Profile', image: ProfileImg },
    { title: 'About', image: AboutImg }
];

const handleTileClick = (title) => {
router.push({ name: 'Complaint', params: { title } });
};
</script>

<template>
      <!-- <NavigationBarView /> -->
      <NavigationBarView2 />
    <div class="home-container">
        <SidePane/>
        <div class="main-pane">
        <BreadCrumb/>
        <div class="tile-container">
            <Tile v-for="(tile, index) in tiles" :key="index" :title="tile.title" :image="tile.image" @tile-clicked="handleTileClick"/>
        </div>
    </div>
    </div>
</template>

<style>
.main-pane{
    display: flex;
    align-items: start;
    flex-direction: column;
}
.home-container {
    justify-content: center;
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
}
</style>
