<script setup>
import { ref, nextTick } from 'vue';
import logo from '../assets/logo.png';

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
    'Home': [
        "More About Worldline",
        "Products",
        "Development",
        "2024 Q1 Roadmap",
        "2024 Q2 Roadmap",
        "Financials",
        "Investors",
    ],
    'About': [
        "About WGS",
        "Our Mission",
        "Our Vision",
        "Our Values",
        "Our Services",
    ],
    'Contact': [
        "Contact Us",
        "Service",
        "Sales",
        "Careers",
        "Partners",
        "Locations",
    ],
    'Dev': [
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
            <router-link @mouseenter="handleMouseEnter" to="/">Home</router-link>
            <router-link @mouseenter="handleMouseEnter" to="/about">About</router-link>
            <router-link @mouseenter="handleMouseEnter" to="/service">Contact</router-link>
            <router-link @mouseenter="handleMouseEnter" to="/dev">Dev</router-link>
            <router-link to="/login" class="nav_special" @mouseenter="handleOptionsMouseLeave">Login</router-link>
        </div>
        <div class="nav_more_options_container" @mouseleave="handleOptionsMouseLeave" :style="moreOptionsStyle">
            <div v-for="(option, index) in more_options[currentOptions]" :key="index">
                <router-link :to="option" class="jos">{{ option }}</router-link>
            </div>
        </div>
    </div>
</template>

<style scoped>
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
    padding: 2rem;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    align-content: center;
    flex-wrap: nowrap;
    flex-direction: row;
    box-shadow: 0 0 0.5rem 0rem var(--wl);
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
    flex-direction: row;
}

.navigation_router_container a {
    padding: 0.7rem 2rem;
    font-size: 1rem;
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