<script setup>
import { computed } from 'vue';

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
});

const current_path = computed(() => {
  return props.data;  
});

console.log(current_path.value);

</script>

<template>
  <ul class="breadcrumb">
    <li class="breadcrumb-item" v-for="(path, title) in current_path" :key="title">
      <router-link :to="path">{{ title }}</router-link>
    </li>
  </ul>    
</template>

<style scoped>
.breadcrumb {
  list-style: none;
  display: flex;
  margin: 0rem 3.4rem;
  margin-bottom: 0.3rem;
  font-size: 0.8rem;
  margin-top: 1rem;
  font-family: wl1;
  font-weight: 100;
  flex-direction: row;
  flex-wrap: nowrap;
  align-content: center;
  justify-content: center;
  align-items: flex-start;
  gap: 0.1rem;
}

.breadcrumb * {
  color: #7d8987;
}

.breadcrumb-item:hover * {
  text-decoration: underline;
}

.breadcrumb-item::before {
  content: '/';    
  padding: 0.1rem;
}

.breadcrumb-item:last-child::after {
  content: '';
}
</style>
