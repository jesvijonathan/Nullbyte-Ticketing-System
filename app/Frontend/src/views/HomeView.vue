<script setup>
import { useAuthStore } from '@/stores/auth';
import Tile from '@/components/Tile.vue';
import SidePane from '@/components/SidePane.vue';
import router  from '../router/';
import BreadCrumb from '@/components/BreadCrumb.vue';
import NavigationBarView from '@/views/NavigationBarView.vue' 


const authStore = useAuthStore();

import CreateTicket from '@/assets/createTicket.svg';
import Ticket from '@/assets/Ticket.png';
import Inbox from '@/assets/Inbox.png';
import Chatbot from '@/assets/chatbot.svg';
import Report from '@/assets/Report.png';
import Alert from '@/assets/Alert.png';
import HelpDesk from '@/assets/Service.png';
import Profile from '@/assets/Profile.png';

const tiles = [
    { title: 'Create Tickets', image: CreateTicket },
    { title: 'Ticket', image: Ticket },
    { title: 'Inbox', image: Inbox },
    { title: 'Chatbot', image: Chatbot },
    { title: 'Report', image: Report },
    { title: 'Alert', image: Alert },
    { title: 'Help Desk', image: HelpDesk },
    { title: 'Profile', image: Profile }
];

const handleTileClick = (title) => {
router.push({ name: 'Complaint', params: { title } });
};
</script>

<template>
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

}
.tile-container {
    display: flex;
    flex-wrap: wrap; 
    justify-content: center;
    margin-top: 20px; 
}
</style>
