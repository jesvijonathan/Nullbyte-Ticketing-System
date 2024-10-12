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
    width: '0'
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
    moreOptionsStyle.value.height = `${more_options[event.target.innerText].length * 3.4}rem`;
    moreOptionsStyle.value.width = "auto";
    currentOptions.value = event.target.innerText;
};

const handleMouseLeave = () => {
    moreOptionsStyle.value.opacity = '0';
    moreOptionsStyle.value.filter = 'blur(0.9rem)';
    moreOptionsStyle.value.height = 
    setTimeout(() => {
        showMoreOptions.value = false;
    }, 300); 
};

const handleOptionsMouseLeave = () => {
    handleMouseLeave();
};

const more_options = {
    'Chatbot': [
        "More About Worldline",
        "Products",
        "Development",
        "2024 Q1 Roadmap",
        "2024 Q2 Roadmap",
        "Financials",
        "Investors",
    ],
    'Tickets': [
        "About WGS",
        "Our Mission",
        "Our Vision",
        "Our Values",
        "Our Services",
    ],
    'Dashboard': [
        "Contact Us",
        "Service",
        "Sales",
        "Careers",
        "Partners",
        "Locations",
    ],
    'Settings': [
        "API",
        "SDK",
        "Documentation",
        "Tutorials",
        "Community",
        "Blog",
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
                <div class="nav_profile"><img class="nav_profile_img" :src="ProfileImg" alt="Profile" title="Profile" /></div>
        </div>
        <!-- <div class="nav_more_options_container" @mouseleave="handleOptionsMouseLeave" :style="moreOptionsStyle">
            <div v-for="(option, index) in more_options[currentOptions]" :key="index">
                <router-link :to="option" class="jos">{{ option }}</router-link>
            </div>
        </div> -->
    </div>
</template>

<style scoped>
.nav_profile{
    height: 2.6rem;
    width: 2.6rem;
    cursor: pointer;
    margin-left: 1.5rem;
    border: 0.1rem solid transparent;
    border-radius: 50%;
    filter: contrast(0.8);
}
.nav_profile:hover{
    border: 0.1rem solid transparent;
    animation: border_rotate 1s infinite;
    background-color: #27a295;
}
.nav_profile:hover .nav_profile_img{
    filter: grayscale(1)  saturate(0) contrast(100) brightness(1);
}
.nav_profile_img{
    height: 2.6rem;
    width: 2.6rem;
    border-radius: 50%;
}
nav
{
   position: fixed;
   top: 0;
}
.nav_more_options_container div{
    padding: 1rem 3rem;
    font-size: 0.9rem;
    color: var(--tertiary);
    text-align: center;
    cursor: pointer;
}
.nav_more_options_container div a{
    transition: 0.1s ease-in-out;
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
    margin-top: 2rem;
    background-color: white;
    z-index: 999;
    transition: all 0.3s ease-in-out;
    padding-bottom: 1rem; 
    overflow: hidden;
    border-radius: 0 0 1rem 1rem;
    border: 0.1rem solid var(--wl);
    border-top: 0.1rem solid white;
    /* box-shadow: 0 0 0.5rem 0rem var(--wl); */
}

.navigation_bar {
    background-color: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10rem);
    padding: 2rem 3rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    align-content: center;
    flex-wrap: nowrap;
    flex-direction: row;
    /* box-shadow: 0 0 0.5rem 0rem var(--wl); */
    border: 0.1rem solid var(--secondary);
    height: 3vh;
}

.wl_logo {
    height: auto;
    cursor: pointer;
    z-index: 100;
}

.navigation_router_container {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    align-content: center;
    flex-wrap: nowrap;
    flex-direction: row
}

.navigation_router_container a {
    padding: 0.7rem 1rem;
    color: #4B8077;
    font-size: 0.8rem;
    border-bottom: 0.1rem solid white;
}

.navigation_router_container a:hover {
    border-bottom: 0.1rem solid var(--wl);
    color: var(--wl);
}

.nav_special {
    background-color: var(--wl);
    color: var(--secondary);
    padding: 0.5rem 2rem;
    border-radius: 1rem;
    border: 0.1rem solid var(--wl);
    transition: 0.1s ease-in-out;
    margin-left: 2rem;
    font-family: wl3;
}

.nav_special:hover {
    background-color: var(--secondary);
    box-shadow: 0 0 0.5rem 0rem var(--wl);
    color: var(--wl);
}
</style>