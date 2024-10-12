<!-- add a router and display views depending on selected url -->
<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import NavigationBarView from './views/NavigationBarView.vue' 
import NavigationBarView2 from './views/NavigationBarView_2.vue' 

const route = useRoute()
</script>

<template>
  

  <body>
    <router-view />
  </body>
</template>

<style scoped>
</style>
