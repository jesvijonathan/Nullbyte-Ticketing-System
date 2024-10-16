<script setup>
import { faL } from '@fortawesome/free-solid-svg-icons';
import { onMounted, ref } from 'vue';

let load_complete = ref(false); 

function kill_loader() {
  const loader_curatin = document.getElementById("loader_curatin");
  const loader_spinner = document.getElementById("loader__spinner");
  
  loader_curatin.style.opacity = 0;
  loader_curatin.style.backdropFilter = "blur(10vw)";
  loader_spinner.style.animation = "none";
  loader_spinner.style.opacity = 0;

  setTimeout(() => {
    loader_curatin.style.display = "none"; 
    load_complete.value = true; 
  }, 1000);
}

function triggerGlitchEffect() {
  const myDiv = document.getElementById('myDiv');

  setInterval(() => {
    myDiv.classList.add('glitch');  
    setTimeout(() => {
      myDiv.classList.remove('glitch'); 
    }, 200);
  }, Math.random() * 5000 + 3000); 
}

let check_loaded = ref(false);


setInterval(() => {
    if (check_loaded.value) {
        kill_loader();
    }
}, 1000);

onMounted(() => {
    check_loaded.value = true;
});

// let feq = ref("0.2s")
let feq = ref("0.7s")

</script>

<template>
  <div v-if="!load_complete" class="loader" id="loader_curatin">
    <div class="loader__container logo_svg" id="loader__spinner">


        <div id="myDiv" v-if="!isLoadComplete">
  <svg>
    <filter id="pixelate" x="0" y="0">
      <feFlood x="4" y="4" height="1" width="1" />
      <feComposite id="composite1" width="10" height="10" />
      <feTile result="a" />
      <feComposite in="SourceGraphic" in2="a" operator="in" />
      <feMorphology id="morphology" operator="dilate" radius="5" />
    </filter>

    <animate xlink:href="#composite1" 
      attributeName="width" from="30" to="10" :dur=feq
      repeatCount="indefinite" fill="freeze" />  
    <animate xlink:href="#composite1" 
      attributeName="height" from="20" to="10" :dur=feq
      repeatCount="indefinite" fill="freeze" />
    <animate xlink:href="#morphology" 
      attributeName="radius" from="20" to="5" :dur=feq
      repeatCount="indefinite" fill="freeze"/>
  </svg>
</div>


</div>
  </div>

</template>




<style scoped>
#myDiv::before{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    height: 10vw;
    width: 100%;
    filter: url(#pixelate);
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    background-image: url(/src/assets/Nullbyte.svg);
    animation: glitch_stope-21219c47 1s infinite forwards;
    display: flex;
    align-items: center;
    justify-content: center;
    align-content: center;
    flex-wrap: nowrap;
    flex-direction: column;
}
@keyframes glitch_stope{
0%{
    filter:url(#pixelate);
}
50%{
    filter:url();
}
60%{
    filter:url(#pixelate);
}
70%{
    filter:url();
}

90%{
    filter:url(#pixelate);
}
100%{
    filter:url();
}
}


#myDiv {
  position:relative;
  transform: scale(0.7);
  animation: scaleLogo 0.45 1 forwards;
  
}

.inside {
  position: relative;
}

.svg_null{
    width: 12vw;   
}
.svg_null path{
    animation: svg_design 4s infinite;
}

.loader {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: linear-gradient(135deg, rgba(122, 122, 122, 0.3), rgba(255, 255, 255, 0.603), rgba(255, 255, 255, 0.9));
  backdrop-filter: blur(5vw);
  z-index: 1000;
  display: flex;
  animation: gradient-rotate 3s infinite linear;
  background-size: 400% 400%;
  transition: opacity 0.5s ease, backdrop-filter 0.5s ease;
  opacity: 1;
}

.loader__container {
    margin: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    transition: 0.3s ease-in-out;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: center;
}

.logo_svg {
  background-position: center;
  height: 6vw;
  background-size: contain;
  animation: scaleLogo 0.5s ease forwards;
}

@keyframes scaleLogo {
  0% {
    transform: scale(0.6);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes gradient-rotate {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.disable-button {
  position: absolute;
  top: 20px;
  right: 20px;
  padding: 10px 20px;
  background-color: #333;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  z-index: 1001;
}

.disable-button:hover {
  background-color: #555;
}
</style>
