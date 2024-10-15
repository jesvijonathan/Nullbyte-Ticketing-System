<template>
  <div class="tile" @click="handleClick">
    <img :src="image" alt="" class="tile-image" />
    <h2 class="tile_text">{{ title }}</h2>
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
/* .tile {
  border-radius: 0.7vw;
  height: 6vw;
  width: 19vw;
  padding: 1vw;
  margin: 1vw;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 0.1vw solid var(--wl);
}
.tile:hover {
  mix-blend-mode: difference;
  border: 0.1vw solid #46beaa00;
  box-shadow: 0 0 0.3vw #46beaa;
  color: #46beaa;
}
.tile:hover * {
  color: #46beaa;
}
.tile-image {
  height:auto;
  padding: 0.8vw;
  max-width: 2.2vw;
  max-height: 2.2vw;
  transition: transform 0.1s ease-in-out;
  width:auto;
  margin-top: 0.2vw;
}
.tile_text{
  font-size: 1vw;
  margin-top: 0.7vw;
  text-align: center;
  font-family: wl1;
} */


.tile {
  border-radius: 0.7vw;
  height: 6vw;
  width: 19vw;
  padding: 1vw;
  margin: 1vw;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 0.1vw solid var(--wl);
}
.tile:hover {
  background-color: #46beaa;
  border: 0.1vw solid #46beaa; 
  mix-blend-mode: difference;
  /* box-shadow: 0 0 0.3vw #46beaa; */
  color: #46beaa;
  /* background-image: linear-gradient(#ffff,#faf9f9,#f0f0f0,#f0f0f0,#46beaa43); */
}
.tile:hover * {
  color: white;
  font-weight: 600;
  font-size: 1.1vw
}
.tile:hover .tile-image {
  /* transform: scale(1.15); */
  /* add tint, it is black and white rn */
  /* filter: sepia(1) hue-rotate(80deg); */
  /* mix-blend-mode: exclusion; */
  transform: scale(0);
  margin-top: 0vw;
  max-width: 0vw;
  max-height: 0vw;
  padding: 0vw;
}
.tile-image {
  height:auto;
  padding: 0.8vw;
  max-width: 2.2vw;
  max-height: 2.2vw;
  width:3.5vw;
  margin-top: 0.2vw;
}
.tile:hover .tile_text{

  margin-top: 0.3vw;
}
.tile_text{
  font-size: 1vw;
  margin-top: 0.7vw;
  text-align: center;
  font-family: wl1;
}
</style>
