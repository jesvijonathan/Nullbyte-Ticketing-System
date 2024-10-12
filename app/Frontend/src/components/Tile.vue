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
  border-radius: 0.7rem;
  height: 6rem;
  width: 19rem;
  padding: 1rem;
  margin: 1rem;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 0.1rem solid var(--wl);
}
.tile:hover {
  mix-blend-mode: difference;
  border: 0.1rem solid #46beaa00;
  box-shadow: 0 0 0.3rem #46beaa;
  color: #46beaa;
}
.tile:hover * {
  color: #46beaa;
}
.tile-image {
  height:auto;
  padding: 0.8rem;
  max-width: 2.2rem;
  max-height: 2.2rem;
  transition: transform 0.1s ease-in-out;
  width:auto;
  margin-top: 0.2rem;
}
.tile_text{
  font-size: 1rem;
  margin-top: 0.7rem;
  text-align: center;
  font-family: wl1;
} */


.tile {
  border-radius: 0.7rem;
  height: 6rem;
  width: 19rem;
  padding: 1rem;
  margin: 1rem;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 0.1rem solid var(--wl);
}
.tile:hover {
  background-color: #46beaa;
  border: 0.1rem solid #46beaa; 
  mix-blend-mode: difference;
  /* box-shadow: 0 0 0.3rem #46beaa; */
  color: #46beaa;
  /* background-image: linear-gradient(#ffff,#faf9f9,#f0f0f0,#f0f0f0,#46beaa43); */
}
.tile:hover * {
  color: white;
  font-weight: 600;
  font-size: 1.1rem
}
.tile:hover .tile-image {
  /* transform: scale(1.15); */
  /* add tint, it is black and white rn */
  /* filter: sepia(1) hue-rotate(80deg); */
  /* mix-blend-mode: exclusion; */
  transform: scale(0);
  margin-top: 0rem;
  max-width: 0rem;
  max-height: 0rem;
  padding: 0rem;
}
.tile-image {
  height:auto;
  padding: 0.8rem;
  max-width: 2.2rem;
  max-height: 2.2rem;
  width:auto;
  margin-top: 0.2rem;
}
.tile:hover .tile_text{

  margin-top: 0.3rem;
}
.tile_text{
  font-size: 1rem;
  margin-top: 0.7rem;
  text-align: center;
  font-family: wl1;
}
</style>
