<script>
import { ref } from 'vue';
import {useAuthStore } from '../stores/auth'
const showPassword = ref(false);

const handleShowPassword = () => {
  showPassword.value = !showPassword.value;
};

const blurBackground=false;

// const schema = Yup.object().shape({
//     username: Yup.string().required('Username is required'),
//     password: Yup.string().required('Password is required')
// });
export default {
data() {
  return {
    email:"",
    password:"",
    errors:""
  };
},
methods:{ async onSubmit() {
    const authStore = useAuthStore();
    console.log(this.email,this.password)
    this.errors=await authStore.login(this.email, this.password)
}}}
</script>


<template>
  <div class="blue_moving_bg" v-if="blurBackground"></div>
  <div class="login-container">
    <!-- <div class="logo"><img src="@/assets/logo.png" alt="Worldline Logo" /></div> -->
    <h2 class="login_info">Log In to NullByte</h2>
    <div class="login-form">
      <form>
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" name="email" v-model="email" placeholder="email@example.com" />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <div class="password-wrapper">
            <input :type="showPassword ? 'text' : 'password'" name="password" v-model="password" id="password" placeholder="password" />
            <button type="button" class="show-password" @click="handleShowPassword">
              <font-awesome-icon :icon="showPassword ? 'eye-slash' : 'eye'" />  
            </button>
            <div class="invalid-feedback">{{ this.errors }}</div>
          </div>
        </div>
        <button type="button" @click="onSubmit" class="login-button">Log In</button>
        <a href="#" class="forgot-password">Forgot Password?</a>
      </form>
    </div>
  </div>
</template>

<style scoped>

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
    /* filter: blur(30rem); */
  }
  50% {
    background-position: 100% 100%;
    transform: rotate(180deg) scale(2);
    filter: blur(30rem);
  }
  100% {
    background-position: 0% 0%;
    transform: rotate(360deg) scale(1);
    
    /* filter: blur(15rem); */
  }
}

.login_info{
  font-size: 1.8rem;
  color: #333;
  font-weight: 900;
  font-family: wl2;
  margin-bottom: 2rem;
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
  margin-top: 9rem;

}

.logo img {
  width: 15rem;
  margin-bottom: 3rem;
}

.login-form {
  background: white;
  padding: 3rem;
  border-radius: 1.2rem;
  border: 0.1rem solid var(--light_grey);
  text-align: center;
  width: 25rem;
}

.login-form h2 {
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
  text-align: left;
}

.form-group label {
  font-family: wl1;
  display: block;
  margin-bottom: 0.5rem;
}

.form-group input {
  font-family: wl1;
  border: 0.1rem solid #ccc;
  border-radius: 5px;
  padding: 0.7rem;
  width: 23rem;
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
  height: 100%;
  border: none;
  background: none;
  cursor: pointer;
  padding: 0 1.3rem;
  color: #333;
}

.show-password:hover{
}

.login-button {
  font-family: wl1;
  width: 100%;
  padding: 0.75rem;
  background-color: #0a8086;
  color: white;
  border: none;
  border-radius: 5rem;
  text-align: center;
  cursor: pointer;
  font-size: 1rem;
  margin-top: 1rem;
}

.login-button:hover {
  background-color: var(--wl);
  /* box-shadow: 0 0 2rem 0.1rem var(--wl); */
}

.forgot-password {
  font-family: wl1;
  text-align: center;
  color: #02656b;
  display: block;
  margin-top: 2rem;
  font-size: 0.9rem;
}

.forgot-password:hover {
  text-decoration: underline;
}
</style>