<script setup>
import BreadCrumb from '@/components/BreadCrumb.vue';
</script>

<template>
    <BreadCrumb/>
    <div class="service-desk-container">
        <div class="service-desk-header">
        <h2>Service Desk</h2>
        </div>
        <div class="service-desk-content">
        <div class="service-desk-sidebar">
            <div class="service-desk-sidebar-item">
            <h3>My Tickets</h3>
            </div>
            <div class="service-desk-sidebar-item">
            <h3>Open Tickets</h3>
            </div>
            <div class="service-desk-sidebar-item">
            <h3>Resolved Tickets</h3>
            </div>
            <div class="service-desk-sidebar-item">
            <h3>Unresolved Tickets</h3>
            </div>
        </div>
        <div class="service-desk-main">
            <div class="service-desk-main-header">
            <h3>My Tickets</h3>
            </div>
            <div class="service-desk-main-content">
            <div class="service-desk-ticket">
                <div class="service-desk-ticket-header">
                <h4>Issue: </h4>
                <h4>Priority: </h4>
                <h4>Status: </h4>
                </div>
                <div class="service-desk-ticket-content">
                <p>Issue Description</p>
                <p>Priority</p>
                <p>Status</p>
                </div>
            </div>
            </div>
        </div>
        </div>
    </div>
    
</template>


<style scoped>
.service-desk-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: 50px;
}
.service-desk-header {
    font-size: 2vw;
    font-weight: 900;
    font-family: wl2;
    margin-bottom: 2vw;
}
.service-desk-content {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
}
.service-desk-sidebar {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-right: 2vw;
}
.service-desk-sidebar-item {
    margin-bottom: 1vw;
    cursor: pointer;
}
.service-desk-main {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.service-desk-main-header {
    font-size: 1.5vw;
    font-weight: 900;
    font-family: wl2;
    margin-bottom: 2vw;
}
.service-desk-main-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.service-desk-ticket {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-bottom: 1vw;
    padding: 1vw;
    border: 0.1vw solid var(--wl);
    border-radius: 1vw;
}
.service-desk-ticket-header {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    width: 100%;
    margin-bottom: 1vw;
}
.service-desk-ticket-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
}
</style>
