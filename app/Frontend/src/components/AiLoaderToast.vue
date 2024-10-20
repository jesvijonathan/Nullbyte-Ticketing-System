<script setup>
import { faL } from '@fortawesome/free-solid-svg-icons';
import { onMounted, ref } from 'vue';

import ai_gif from '@/assets/ai.gif';

const props = defineProps({
  loading: {
    type: Boolean,
    required: true
  }
});
</script>

<template>
  <div class="loader" v-if="loading">
    <div class="loader_con">
        <img :src="ai_gif" alt="AI Loader" height="100%">
        <div style="font-size: 1.1vw; color: grey;">
          Using AI<span class="dot dot1">.</span><span class="dot dot2">.</span><span class="dot dot3">.</span>
        </div>
      </div>
  </div>
</template>

<style scoped>
.loader {
    position: fixed;
    z-index: 999;
    top: 8vw;
    width: 75vw;
    left: 23%;
    border: 0.2vw solid #f3f3f331;
    background-color: rgba(255, 255, 255, 0.3);
    border-radius: 0.3vw;
    height: 87vh;
    backdrop-filter: blur(0.3vw);
    display: flex;
    justify-content: center;
    align-items: center;
}

.loader_con:hover{
    cursor: pointer;
    background-color: rgb(240, 240, 240);
}

.loader_con {
    height: 10vw;
    padding: 2.3vw 1.5vw;
    gap: 2vw;
    width: 10vw;
    background-color: rgb(250, 250, 250);
    border: 0.1vw solid #dfdfdf;
    display: flex;
    border-radius: 0.5vw;
    flex-direction: column;
    align-items: center;
    justify-content: space-evenly;
}

.loader_con img {
    border-radius: 50%;
    width: 6vw;
    height: 6vw;
    animation: rotate 5s linear infinite;
}

@keyframes rotate {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Dots animation */
.dot {
    display: inline-block;
    animation: dot-blink 1.5s infinite step-start;
}

.dot1 {
    animation-delay: 0s;
}

.dot2 {
    animation-delay: 0.3s;
}

.dot3 {
    animation-delay: 0.6s;
}

@keyframes dot-blink {
    0% { opacity: 0; }
    50% { opacity: 1; }
    100% { opacity: 0; }
}
</style>
