<template>
  <div class="tile" @click="handleClick">
    <img :src="image" alt="" class="tile-image" />
    <h2>{{ title }}</h2>
  </div>
</template>

<script>
export default {
  name: 'Tile',
  props: {
      title: {
          type: String,
          required: true
      },
      image: {
          type: Image,
          required: true
      }
  },
  methods: {
      handleClick() {
          this.$emit('tile-clicked', this.title);
      }
  }
};
</script>

<style scoped>
.tile {
  border: 1px solid #ccc;
  border-radius: 9px;
  height: 100px;
  width: 300px;
  padding: 20px;
  margin: 10px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  transition: transform .2s;
}
.tile:hover {
  background-color: #ffffff;
  transform: scale(1.1);
  /* background-image: linear-gradient(#ffff,#faf9f9,#f0f0f0,#f0f0f0,#46beaa43); */
}
.tile-image {
  height:auto;
  padding: 5px;
  max-width: 150px;
  max-height: 150px;
  width:auto;
  margin-top: 5px;
}
</style>
