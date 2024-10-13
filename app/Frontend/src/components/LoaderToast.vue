<script setup>
import { faL } from '@fortawesome/free-solid-svg-icons';
import { onMounted, ref } from 'vue';

const props = defineProps({
  loading: {
    type: Boolean,
    required: true
  }
});

</script>
<template>
  <div :class="loading ? 'loader' : 'loader hidden'"></div>
</template>

<style scoped>
.loader {
    position: fixed;
    z-index: 999;
  border: 0.2rem solid #f3f3f331;
  border-top: 0.2rem solid var(--wl);
  border-radius: 50%;
  width: 1.4rem;
  height: 1.4rem;
  animation: spin 2s linear infinite;
  transform: translate(-50%, -50%);
    top: 95%;
    left: 2rem;

    animation: spin 1s linear infinite;
    cursor: pointer;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.hidden{
    display: none;
}
</style>
