<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import NavigationBarView from '@/views/NavigationBarView.vue';
import { useCookies } from 'vue3-cookies';

const showPassword = ref(false);
const { cookies } = useCookies();

const handleShowPassword = () => {
  showPassword.value = !showPassword.value;
};

const blurBackground = ref(false);

let email = ref("");
let password = ref("");
let errors = ref("");

async function SubmitLogin() {
  const authStore = useAuthStore();


  try {
    errors.value = await authStore.login(email.value, password.value);
    cookies.set('email', email.value);

  } catch (error) {
    errors.value = "Login failed. Please try again.";
  }
}

</script>



<template>
      <NavigationBarView />
  <div class="blue_moving_bg" v-if="blurBackground"></div>
  <div class="login-container">
    <!-- <div class="logo"><img src="@/assets/logo.png" alt="Worldline Logo" /></div> -->
    <h2 class="login_info">Log In to NullByte</h2>
    <div class="login-form">
      <form @submit.prevent="SubmitLogin">
        <div class="form-group">
          <label for="email">Email</label>
          <input type="text" id="email" name="email" v-model="email" placeholder="email@example.com" />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <div class="password-wrapper">
            <input :type="showPassword ? 'text' : 'password'" name="password" v-model="password" id="password" placeholder="password" />
            <button type="button" class="show-password" @click="handleShowPassword()">
              <font-awesome-icon :icon="showPassword ? 'eye-slash' : 'eye'" />  
            </button>
            <div class="invalid-feedback">{{ errors }}</div>
          </div>
        </div>
        <button type="submit" class="login-button">Log In</button>
        <a href="#" class="forgot-password">Forgot Password?</a>
      </form>
    </div>
  </div>
</template>

<style scoped>

.invalid-feedback{
  color: red;
  font-size: 0.8vw;
  text-align: center;
  margin-top: 1vw;
  font-weight: light;
  font-family: wl1;
  z-index: -1;
}
.blue_moving_bg{
  position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to bottom right, #ffffff, #02666b);
    z-index: -1; 
    animation: moving 10s infinite;
    opacity: 0.4;
}
@keyframes moving {
  0% {
    background-position: 0% 0%;
    transform: rotate(0deg) scale(1.1);
    /* filter: blur(30vw); */
  }
  50% {
    background-position: 100% 100%;
    transform: rotate(180deg) scale(2);
    filter: blur(30vw);
  }
  100% {
    background-position: 0% 0%;
    transform: rotate(360deg) scale(1);
    
    /* filter: blur(15vw); */
  }
}

.login_info{
  font-size: 1.8vw;
  color: #333;
  font-weight: 900;
  font-family: wl2;
  margin-bottom: 2vw;
}
body, html {
  height: 100%;
  margin: 0;
  font-family: Arial, sans-serif;
}

.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  margin-top: 9vw;

}

.logo img {
  width: 15vw;
  margin-bottom: 3vw;
}

.login-form {
  background: white;
  padding: 3vw;
  border-radius: 1.2vw;
  border: 0.1vw solid var(--light_grey);
  text-align: center;
  width: 25vw;
}

.login-form h2 {
  margin-bottom: 1.5vw;
  font-size: 1.5vw;
  color: #333;
}

.form-group {
  margin-bottom: 1vw;
  text-align: left;
}

.form-group label {
  font-family: wl1;
  display: block;
  margin-bottom: 0.5vw;
}

.form-group input {
  font-family: wl1;
  border: 0.1vw solid #ccc;
  border-radius: 0.3vw;
  padding: 0.7vw;
  width: 23vw;
}

.form-group input:focus {
  outline: none;
  border-color: var(--wl);
}

.password-wrapper {
  position: relative;
}

.show-password {
  position: absolute;
  top: 0;
  right: 0;
  height: 3vw;
  border: none;
  background: none;
  cursor: pointer;
  padding: 0 1.3vw;
  color: #333;
}

.show-password:hover{
}

.login-button {
  font-family: wl1;
  width: 100%;
  padding: 0.75vw;
  background-color: #0a8086;
  color: white;
  border: none;
  border-radius: 5vw;
  text-align: center;
  cursor: pointer;
  font-size: 1vw;
  margin-top: 1vw;
}

.login-button:hover {
  background-color: var(--wl);
  /* box-shadow: 0 0 2vw 0.1vw var(--wl); */
}

.forgot-password {
  font-family: wl1;
  text-align: center;
  color: #02656b;
  display: block;
  margin-top: 2vw;
  font-size: 0.9vw;
}

.forgot-password:hover {
  text-decoration: underline;
}
</style>