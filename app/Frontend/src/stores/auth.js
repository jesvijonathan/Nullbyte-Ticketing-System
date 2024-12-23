import { defineStore } from 'pinia';
import router  from '../router/';
import { jwtDecode } from "jwt-decode";
import { useCookies } from 'vue3-cookies';

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => {
        const user = JSON.parse(localStorage.getItem('user'));
        return {
            user: user,
            username: user ? jwtDecode(user.token).username : null,
            upn:user ? jwtDecode(user.token).upn:[]
        };
    },
    getters: {  
        isAuthenticated: (state) => !!state.user
    },
    actions: {
        async login(email, password) {
            const requestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            };
            const response = await fetch(document.baseMyURL  + "/sso/auth", requestOptions);
            console.log(response);
            if (!response.ok) {
                if (response.status == 401)
                    return "Invalid credentials!";
                else
                    return "Unknown Error! Try again later";
            }

            const user = await response.json();
            console.log(user.token);
            this.user = user.token ? user : null;
            this.username=jwtDecode(user.token).username
            localStorage.setItem('user', JSON.stringify(this.user));
            const { cookies } = useCookies();
            cookies.set('token', user.token);
            cookies.set('session', user.token);
            cookies.set('user', jwtDecode(user.token).username);
            cookies.set('upn', jwtDecode(user.token).upn);
            cookies.set('role', jwtDecode(user.token).role);
            cookies.set('exp', jwtDecode(user.token).exp);
            cookies.set('iat', jwtDecode(user.token).iat);

            router.push('/dashboard');
            return "";
        },
        async logout() {
            this.user = null;
            localStorage.removeItem('user');
            // remove cookies
            const { cookies } = useCookies();
            cookies.remove('token');
            cookies.remove('user');
            cookies.remove('upn');
            cookies.remove('role');
            cookies.remove('exp');
            cookies.remove('iat');
            router.push('/login');
        }
    }
});