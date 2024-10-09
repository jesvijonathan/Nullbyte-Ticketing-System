<template>
    <nav aria-label="breadcrumb">
      <ol class="breadcrumb">
        <li v-for="(item, index) in breadcrumbs" :key="index" class="breadcrumb-item">
          <router-link v-if="index < breadcrumbs.length - 1" :to="item.path">
            {{ item.name }}
          </router-link>
          <span v-else>{{ item.name }}</span>
        </li>
      </ol>
    </nav>
  </template>
  
  <script>
  import { computed } from 'vue';
  import { useRoute } from 'vue-router';
  
  export default {
    name: 'Breadcrumb',
    setup() {
      const route = useRoute();
  
      const breadcrumbs = computed(() => {
        return route.meta.breadcrumb || [];
      });
  
      return {
        breadcrumbs
      };
    }
  }
  </script>
  
  <style scoped>
  .breadcrumb {
    list-style: none;
    display: flex;
    padding:10px;
    color:black;
  }
  
  .breadcrumb-item {
    margin-right: 2px;
    transition: transform 0.3s, color 0.3s;
  }
  
  .breadcrumb-item:hover {
    transform: scale(1.1); 
    text-emphasis-color: green;
  }
  
  .breadcrumb-item::before {
    content: '/';
    margin-left: 2px;
  }
  
  .breadcrumb-item:last-child::after {
    content: '';
  }
  </style>
  