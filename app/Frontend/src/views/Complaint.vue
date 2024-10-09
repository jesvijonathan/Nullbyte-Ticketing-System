<template>
    <div class="complaint-container">
        <h2>Submit a Complaint</h2>
        <form @submit.prevent="submitComplaint">
            <div class="form-group">
                <label for="name">Name</label>
                <input type="text" id="name" v-model="name" required />
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" id="email" v-model="email" required />
            </div>
            <div class="form-group">
                <label for="complaint">Complaint</label>
                <textarea id="complaint" v-model="complaint" required></textarea>
            </div>
            <button type="submit">Submit</button>
        </form>
        <div v-if="message" class="message">{{ message }}</div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const name = ref('');
const email = ref('');
const complaint = ref('');
const message = ref('');

const submitComplaint = async () => {
    try {
        // Replace with your API endpoint
        const response = await fetch('https://your-api-endpoint.com/complaints', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name.value,
                email: email.value,
                complaint: complaint.value,
            }),
        });

        if (response.ok) {
            message.value = 'Complaint submitted successfully!';
            name.value = '';
            email.value = '';
            complaint.value = '';
        } else {
            message.value = 'Failed to submit complaint. Please try again.';
        }
    } catch (error) {
        message.value = 'An error occurred. Please try again.';
    }
};
</script>

<style scoped>
.complaint-container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
    background-color: #f9f9f9;
}

h2 {
    text-align: center;
    color: #333;
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
}

button {
    display: block;
    width: 100%;
    padding: 10px;
    background-color: #46BEAA;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

button:hover {
    background-color: #3ca08e;
}

.message {
    margin-top: 20px;
    text-align: center;
    color: green;
}
</style>