<script setup>
import { useAuthStore } from '@/stores/auth';
import Tile from '@/components/Tile.vue';
import SidePane from '@/components/SidePane.vue';
import router  from '../router';
import BreadCrumb from '@/components/BreadCrumb.vue';
import NavigationBarView from '@/views/NavigationBarView.vue' 
import NavigationBarView2 from '@/views/NavigationBarView_2.vue' 


const authStore = useAuthStore();

import CreateTicketImg from '@/assets/createTicket.svg';
import TicketImg from '@/assets/Ticket.png';

import VertexAI from '@/assets/vertex_ai.webp';
import Llama from '@/assets/llama3.png';
import StartCon from '@/assets/startcon.jpg';

const tiles = [
    { title: 'WL - Vertex AI', image: VertexAI, link: '/vertex' },
    { title: 'WL - LLamma', image: Llama, link: '/llama' },
    { title: 'Start Conversation', image: StartCon, link: '/vertex' },
];

const handleTileClick = (title) => {
    const tile = tiles.find(tile => tile.title === title);
    router.push(tile.link);
};


let bread_path_json={
    "NULLBYTE": "/",
    "CHATBOT": "/chatbot",
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
            <Tile v-for="(tile, index) in tiles" :key="index" :title="tile.title" :image="tile.image" @click="handleTileClick(tile.title)" />
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
    margin-left: 4rem;
}
</style>
