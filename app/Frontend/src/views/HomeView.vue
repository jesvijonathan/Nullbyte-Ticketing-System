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
    { title: 'Create Tickets', image: CreateTicketImg, link: '/create_ticket' },
    { title: 'Ticket', image: TicketImg, link: '/ticket' },
    { title: 'Inbox', image: InboxImg, link: '/inbox' },
    { title: 'Chatbot', image: ChatbotImg, link: '/chatbot' },
    { title: 'Report', image: ReportImg, link: '/report' },
    { title: 'Alert', image: AlertImg, link: '/alert' },
    { title: 'Help Desk', image: HelpDeskImg, link: '/helpdesk' },
    { title: 'Profile', image: ProfileImg, link: '/profile' },
    { title: 'About', image: AboutImg, link: '/about' },
];

const handleTileClick = (title) => {
    const tile = tiles.find(tile => tile.title === title);
    router.push(tile.link);
};


let bread_path_json={
    "NULLBYTE": "/",
    "DASHOARD": "/dashboard",
} 
</script>

<template>
      <!-- <NavigationBarView /> -->
      <NavigationBarView2 />
    <div class="home-container">
        <SidePane/>
        <div class="main-pane">
        <BreadCrumb :data="bread_path_json"/>
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
}
</style>
