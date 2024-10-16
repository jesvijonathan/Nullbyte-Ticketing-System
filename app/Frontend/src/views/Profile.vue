<script setup>
import { useAuthStore } from '@/stores/auth';
import SidePane from '@/components/SidePane.vue';
import BreadCrumb from '@/components/BreadCrumb.vue';
import NavigationBarView2 from '@/views/NavigationBarView_2.vue';
import { ref, onMounted, watch } from 'vue';
import { useCookies } from 'vue3-cookies';


const current_user = ref(null);
const { cookies } = useCookies();
const authStore = useAuthStore();

let bread_path_json = {
    "NULLBYTE": "/",
    "SETTINGS": "/profile",
    "PROFILE": "/profile"
};

if (!current_user.value) {
    current_user.value = cookies.get('user');
    if (!current_user.value) {
        alert('Please login again to continue, could not find user details');
    }
}

const profile = ref({
    "name": "Jesvi Jonathan",
    "username": "jesvi",
    "email": "jesvin@nullbyte.com",
    "phone": "1234567890",
    "gcm": "5",
    "score": "5",
    "experience": "7",
    "role": "Admin",
    "department": "IT",
    "Team": ["Titan", "Fulcrum", "Nullbyte"],
    "location": "Chennai",
    "status": "Active",
    "organization": "Nullbyte",
    "created": "2021-10-10",
    "updated": "2021-10-10"
})

</script>

<template>
    <NavigationBarView2 />
    <div class="home-container">
        <SidePane />
        <div class="main-pane">
            <BreadCrumb :data="bread_path_json" />
            <div class="prof_con">
                <img src="https://img.icons8.com/?size=100&id=ckaioC1qqwCu&format=png&color=000000" alt="Avatar" style="width: 5vw; height: 5vw; border-radius: 50%;" />
                <div class="prof_con_grp">
                    <div class="prof_con_text">User Information</div>
                    <div class="prof_con_elem">
                        <label>Name</label>
                        <input v-model="profile.name" />
                    </div>
                    <div class="prof_con_elem">
                        <label>Username</label>
                        <input v-model="profile.username" />
                    </div>
                    <div class="prof_con_elem">
                        <label>Email</label>
                        <input v-model="profile.email" />
                    </div>
                    <div class="prof_con_elem">
                        <label>Phone</label>
                        <input v-model="profile.phone" />
                    </div>
                </div>


                <div class="prof_con_grp">
                    <div class="prof_con_text">More Details</div>
                    <div class="prof_con_elem">
                        <label>GCM</label>
                        <input v-model="profile.gcm" type="number" />
                    </div>
                    <div class="prof_con_elem">
                        <label>Score</label>
                        <input v-model="profile.score" type="number" />
                    </div>
                    <div class="prof_con_elem">
                        <label>Experience</label>
                        <input v-model="profile.experience" type="number" />
                    </div>
                    <div class="prof_con_elem">
                        <label>Role</label>
                        <input v-model="profile.role" />
                    </div>
                    <div class="prof_con_elem">
                        <label>Department</label>
                        <input v-model="profile.department" />
                    </div>
                    <div class="prof_con_elem">
                        <label>Team</label>
                        <input v-model="profile.Team" />
                    </div>
                    <div class="prof_con_elem">
                        <label>Status</label>
                        <select v-model="profile.status">
                            <option value="Active">Active</option>
                            <option value="Inactive">Inactive</option>
                            <option value="Suspended">Suspended</option>
                        </select>
                    </div>
                    <div class="prof_con_elem">
                        <label>Location</label>
                        <input v-model="profile.location" />
                    </div>

                    <div class="prof_con_elem">
                        <label>Organization</label>
                        <input v-model="profile.organization" />
                    </div>
                </div>



                <div class="prof_con_grp">
                    <div class="prof_con_text">Account</div>
                    <div class="prof_con_elem">
                        <label>Created</label>
                        <input v-model="profile.created" readonly disabled />
                    </div>
                    <div class="prof_con_elem">
                        <label>Updated</label>
                        <input v-model="profile.updated" readonly disabled/>
                    </div>
                    <br><br><br><br>
                    <div class="prof_con_elem">
                        <button>Logout</button>
                        <button>Reset Account</button>
                        <button>Delete Profile</button>
                        <button>Save Profile</button>
                        <button>Download</button>
                    </div>
                </div>

            </div>
        </div>
    </div>


</template>



<style scoped>
.prof_con_elem button{
    padding: 0.4vw 2vw;
    border-radius: 0.5vw;
    border: 0.1vw solid #cccccc00;
    background-color: rgba(104, 104, 104, 0.515)  ;
    color: white;
    font-size: 1vw;
    font-family: wl1;
    cursor: pointer;
}
.prof_con_elem button:hover{
    background-color: rgba(104, 104, 104, 0.815);
}
.prof_con_elem {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin-top: 1vw;
    margin-bottom: 1vw;
    width: 100%;
    gap: 2vw;
}
.prof_con_elem label {
    font-size: 1vw;
    /* font-weight: 600; */
    font-family: wl3;

}
.prof_con_elem select {
    width: 52vw;
    padding: 1vw;
    border-radius: 0.5vw;
    border: 0.1vw solid #cccccc00;
    background-color: #f5f5f5;
    font-size: 1vw;
    /* font-weight: 600;     */
    font-family: wl1;

}
.prof_con_elem:hover select {
    background-color: #dadada;
}
.prof_con_elem select:focus {
    outline: none;
    border-color: #27a295;
}
.prof_con_elem input {
    width: 50vw;
    padding: 1vw;
    border-radius: 0.5vw;
    border: 0.1vw solid #cccccc00;
    background-color: #f5f5f5;
    font-size: 1vw;
    /* font-weight: 600;     */
    font-family: wl1;

}
.prof_con_elem input:focus {
    outline: none;
    border-color: #27a295;
}
.prof_con_elem:hover input {
    background-color: #dadada;
}
.prof_con_grp {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-top: 2vw;
    margin-left: 2vw;
    margin-right: 2vw;
    padding: 2vw;
    border-radius: 1vw;
    /* gap: 2vw; */
    /* background-color: #f5f5f5; */
    /* box-shadow: 0 0 1vw rgba(0, 0, 0, 0.1); */
}
.prof_con_text {
    font-size: 1.5vw;
    font-weight: 600;
    margin-bottom: 1vw;
    font-family: wl2;
}
.prof_con {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin-top: 2vw;
    margin-left: 2vw;
    margin-right: 2vw;
    padding: 2vw;
    border-radius: 1vw;
    gap: 0vw;
    /* background-color: #f5f5f5; */
    /* box-shadow: 0 0 1vw rgba(0, 0, 0, 0.1); */
}

.prof_con_elem {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin-top: 1vw;
    margin-bottom: 1vw;
    width: 100%;
}

.main-pane {
    display: flex;
    align-items: start;
    flex-direction: column;
    overflow: auto;
    width: -webkit-fill-available;
}

.home-container {
    justify-content: flex-start;
    display: flex;
    flex-direction: row;
    overflow: hidden;
    height: 90vh;
}

.tile-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    overflow-x: hidden;
    overflow-y: auto;
}
</style>

