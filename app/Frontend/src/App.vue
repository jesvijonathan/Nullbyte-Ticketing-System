<!-- add a router and display views depending on selected url -->
<script setup>
import { useRoute } from 'vue-router'
import { computed } from 'vue'
import NavigationBarView from './views/NavigationBarView.vue' 
import NavigationBarView2 from './views/NavigationBarView_2.vue' 

const route = useRoute()

// if load compelte, show the view
import Loader from './components/loader.vue'

const isLoadComplete = false;
// computed(() => {
//   return true
// })

</script>

<template>
  
<Loader/>
  <body>
    <router-view />
  </body>
</template>

<style scoped>
</style>
