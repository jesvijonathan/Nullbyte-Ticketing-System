import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { watch, nextTick } from "vue";

import JOS from "jos-animation"; // jos-animation/dist/jos.debug.js

import App from './App.vue'
import router from './router'

import { library } from "@fortawesome/fontawesome-svg-core";
import { fas } from "@fortawesome/free-solid-svg-icons";
import { far } from "@fortawesome/free-regular-svg-icons";
import { fab } from "@fortawesome/free-brands-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

library.add(fas, far, fab); // Add all the icon packs at once


createApp(App)
  .component("font-awesome-icon", FontAwesomeIcon) // Register the component globally
  .use(createPinia())
  .use(router)
  .mount("#app");

JOS.init();
JOS.version();

watch(
    () => router.currentRoute.value,
    () => {
      nextTick(() => {
        JOS.refresh();
      });
    }
  );
  
