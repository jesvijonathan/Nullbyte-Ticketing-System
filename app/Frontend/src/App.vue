<!-- add a router and display views depending on selected url -->
<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import NavigationBarView from './views/NavigationBarView.vue' 

const route = useRoute()
</script>

<template>
  
  <NavigationBarView />
  <body>
    <router-view />
  </body>
</template>

<style scoped>
</style>
