import { defineStore } from 'pinia';

import router  from '../router/';

const baseUrl = 'http://localhost:5000';

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        user: JSON.parse(localStorage.getItem('user')),
    }),
    getters: {
        isAuthenticated: (state)=> !!state.user
    },
    actions: {
        async login(email, password) {
            const requestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
              };
              const response = await fetch(`${baseUrl}/sso/auth`, requestOptions);
              console.log(response)
              if (!response.ok) { 
                if(response.status==401)
                return "Invalid credentials"
                else
                return "Unknown Error Try again later"
            }

            const user = await response.json(); 
            this.user = user.token ? user : null;

            localStorage.setItem('user', JSON.stringify(this.user));
            router.push('/service');
        return ""
        },
        async logout() {
            this.user = null;
            localStorage.removeItem('user');
            router.push('/login');
        }
    }
});