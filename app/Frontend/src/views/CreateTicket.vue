<script setup>
import BreadCrumb from '@/components/BreadCrumb.vue';
import NavigationBarView from '@/views/NavigationBarView.vue'
import NavigationBarView2 from '@/views/NavigationBarView_2.vue'
import { useAuthStore } from '@/stores/auth';
import SidePane from '@/components/SidePane.vue';


let bread_path_json={
    "NULLBYTE": "/",
    "TICKETS": "/tickets",
    "CREATE TICKET": "/create_ticket",
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

<style scoped>
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
</style>