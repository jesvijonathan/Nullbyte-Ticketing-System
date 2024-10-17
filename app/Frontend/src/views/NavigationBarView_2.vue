<script setup>
import { ref, nextTick } from 'vue';
import logo from '../assets/logo.png';
import { useAuthStore } from '@/stores/auth';
import ProfileImg from '@/assets/profile_nav.png';

const authStore = useAuthStore();

const showMoreOptions = ref(false);
const moreOptionsStyle = ref({
    top: '0',
    left: '0',
    opacity: '0',
    height: '0',
    width: '0',
    zIndex: '-99',
});

const currentOptions = ref('');

const handleMouseEnter = async (event) => {
    showMoreOptions.value = true;
    const rect = event.target.getBoundingClientRect();
    await nextTick();
    moreOptionsStyle.value.zIndex = '999';
    moreOptionsStyle.value.top = `${rect.bottom}px`;
    moreOptionsStyle.value.left = `${rect.left}px`;
    moreOptionsStyle.value.opacity = '1';
    moreOptionsStyle.value.filter = 'blur(0)';
    moreOptionsStyle.value.height = `${more_options[event.target.innerText].length * 3.4}vw`;
    moreOptionsStyle.value.width = "auto";
    currentOptions.value = event.target.innerText;
};

const handleMouseLeave = () => {
    moreOptionsStyle.value.opacity = '0';
    moreOptionsStyle.value.filter = 'blur(0.9vw)';
    moreOptionsStyle.value.height = "0";

};

const handleOptionsMouseLeave = () => {
    handleMouseLeave();
        setTimeout(() => {
        showMoreOptions.value = false;
    }, 300); 
};

const more_options = {
    'Chatbot': [
        "WL Vertex AI",
        "WL LLama",
        "AutoFill",
        "Document Analyser",
    ],
    'Tickets': [
        "Create Ticket",
        "View Tickets",
        "Approval"
    ],
    'Dashboard': [
        "Analytics",
        "Reports",
        "Alerts",
        "Help Desk",
    ],
    'Settings': [
        "Profile",
        "Account",
        "Notifications",
        "Security",
        "Logout",
    ],
};
</script>

<template>
    <div class="navigation_bar" @mouseleave="handleMouseLeave">
        <img :src="logo" class="wl_logo" alt="wl_logo" title="wl_logo" @click="$router.push('/')" />
        <div class="navigation_router_container">
            <router-link @mouseenter="handleMouseEnter" to="/">Chatbot</router-link>
            <router-link @mouseenter="handleMouseEnter" to="/tickets">Tickets</router-link>
            <router-link @mouseenter="handleMouseEnter" to="/dashboard">Dashboard</router-link>
            <router-link @mouseenter="handleMouseEnter" to="/settings">Settings</router-link>
                <div class="nav_profile" @click="$router.push('/profile')"  @mouseenter="handleOptionsMouseLeave"><div style="display: none;">Profile</div><img class="nav_profile_img" :src="ProfileImg" alt="Profile" title="Profile" /></div>
        </div>
        <div class="nav_more_options_container" @mouseleave="handleOptionsMouseLeave" :style="moreOptionsStyle">
            <div v-for="(option, index) in more_options[currentOptions]" :key="index">
                <router-link :to="option" class="jos">{{ option }}</router-link>
            </div>
        </div>
    </div>
</template>

<style scoped>
.nav_profile{
    height: 2.6vw;
    width: 2.6vw;
    cursor: pointer;
    margin-left: 1.5vw;
    border: 0.1vw solid transparent;
    border-radius: 50%;
    filter: contrast(0.8);
}
.nav_profile:hover{
    border: 0.1vw solid transparent;
    animation: border_rotate 1s infinite;
    background-color: #27a295;
}
.nav_profile:hover .nav_profile_img{
    filter: grayscale(1)  saturate(0) contrast(100) brightness(1);
}
.nav_profile_img{
    height: 2.6vw;
    width: 2.6vw;
    border-radius: 50%;
}
nav
{
   position: fixed;
   top: 0;
}
.nav_more_options_container div{
    padding: 1vw 3vw;
    font-size: 0.9vw;
    color: var(--tertiary);
    text-align: center;
    cursor: pointer;

}
.nav_more_options_container div a{
    transition: 0.1s ease-in-out;
    color: CADETBLUE;
}
.nav_more_options_container div:hover {
    background-color: var(--wl);
}
.nav_more_options_container div:hover a {
    background-color: var(--wl);
    color: var(--secondary);
}
.nav_more_options_container {
    position: absolute;
    margin-top: 1.5vw;
    background-color: rgba(255, 255, 255, 0.9);
    transition: all 0.3s ease-in-out;
    padding-bottom: 1vw; 
    overflow: hidden;
    border-radius: 0 0 1vw 1vw;
    border: 0.1vw solid var(--wl);
    border-top: 0.1vw solid white;
    /* box-shadow: 0 0 0.5vw 0vw var(--wl); */
}

.navigation_bar {
    background-color: rgb(255, 255, 255);
    padding: 2vw 3vw;
    display: flex;
    justify-content: space-between;
    align-items: center;
    align-content: center;
    flex-wrap: nowrap;
    flex-direction: row;
    /* box-shadow: 0 0 0.5vw 0vw var(--wl); */
    border: 0.1vw solid var(--secondary);
    height: 3vh;
}

.wl_logo {
    height: 1.4vw;
    cursor: pointer;
    z-index: 100;
}

.navigation_router_container {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    align-content: center;
    flex-wrap: nowrap;
    flex-direction: row;
    
}

.navigation_router_container a {
    padding: 0.7vw 1vw;
    color: #4B8077;
    font-size: 0.8vw;
    border-bottom: 0.1vw solid white;
}

.navigation_router_container a:hover {
    border-bottom: 0.1vw solid var(--wl);
    color: var(--wl);
}

.nav_special {
    background-color: var(--wl);
    color: var(--secondary);
    padding: 0.5vw 2vw;
    border-radius: 1vw;
    border: 0.1vw solid var(--wl);
    transition: 0.1s ease-in-out;
    margin-left: 2vw;
    font-family: wl3;
}

.nav_special:hover {
    background-color: var(--secondary);
    box-shadow: 0 0 0.5vw 0vw var(--wl);
    color: var(--wl);
}
</style>