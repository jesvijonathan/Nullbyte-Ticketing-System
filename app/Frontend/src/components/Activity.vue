<script setup>
import { toRefs, ref, defineEmits } from 'vue';
import { defineProps } from 'vue';
import { computed } from 'vue';


// Get the comment list from the parent component via props
const props = defineProps({
    comments: {
        type: Array,
        required: true
    }
});

const comments = computed(() => {
  return props.comments;
});

// A function to format the date nicely
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};


const emit = defineEmits(['add-comment']);
const newcomment = ref('');

const addComment = () => {
  // Emit an event to the parent component with the new comment
  if (newcomment.value.trim() !== '') {
    emit('add-comment', newcomment.value);
    newcomment.value = '';
    setTimeout(() => {
      const commentList = document.querySelector('.comment-list');
      commentList.scrollTop = commentList.scrollHeight;
    }, 100);

  }
};
// You can add more logic here if needed (e.g., add new comments).
</script>

<template>
  <div class="comments-container">
    <ul class="comment-list">
      <li v-for="comment in comments" :key="comment.comment_id" class="comment-item">
        <div class="comment-header">
          <span class="comment-user">{{ comment.user }} - </span>
          <span class="comment-date">{{ formatDate(comment.date) }}</span>
        </div>
        <div class="comment-text">{{ comment.text }}</div>
      </li>
    </ul>
    <div class="comment-input">
            <input type="text" placeholder="Add a comment..." v-model="newcomment" />
            <button :class="{ enabled: newcomment.trim() !== '' }" 
                    :disabled="newcomment.trim() === ''" 
                    @click="addComment">Send</button>
        </div>
  </div>
</template>

<style scoped>
.comment-input {
    display: flex;
    gap: 0.5vw;
    margin-top: 1vw;
    width: -webkit-fill-available;
    position: fixed;
    bottom: 0;
    padding-bottom: 1.6vw;
    width: 20vw;
    background-color: white;
}

.comment-input input {
    width: 100%;
    /* padding: 0.5vw; */
    border: 0.1vw solid #c4c4c4;
    border-radius: 0.3vw;
    font-size: 0.6vw;
    padding: 0vw 0.5vw;
    font-family: 'wl1';
    color: #333;
}

.comment-input input:focus {
    outline: none;
    border-color: #27a295;
}

.comment-input button {
    padding: 0.5vw 1vw;
    color: white;
    border: none;
    border-radius: 0.3vw;
    font-size: 0.6vw;
    cursor: pointer;
    background-color: #63636347;
}

.comment-input button.enabled {
    background-color: #27a295;
}

.comment-input button:hover.enabled {
    background-color: #1e7e75;
}

.comments-container {
    padding: 1vw;
    padding-bottom: 1.8vw;
    border-radius: 0.5vw;
    margin-top: 0vw;
    height: -webkit-fill-available;
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}

h3 {
    font-size: 0.5vw;
    margin-bottom: 1vw;
    color: #333;
}

.comment-list {
    list-style-type: none;
    padding: 0;
    display: flex;
    gap: 1vw;
    flex-direction: column;
    flex-wrap: nowrap;
    align-content: flex-start;
    justify-content: flex-start;
    align-items: flex-start;

    max-height: webkit-fill-available;
    overflow-y: auto;
    overflow-x: hidden;
    padding-right: 1vw;
    height: calc(100% - 2.8vw);
}
.comment-list::-webkit-scrollbar {
    width: 0.3vw;
    display: none;
}

.comment-list:hover::-webkit-scrollbar {
    display: block;
}
.comment-list::-webkit-scrollbar-thumb {
    background-color: #c4c4c4;
    border-radius: 0.25vw;
}
.comment-list::-webkit-scrollbar-track {
    background-color: #f5f5f5;
}


.comment-item {
    /* border-bottom: 0.1vw solid #525252; */
    border-bottom: 0.01vw solid #c4c4c467;
    width: 18vw;
    padding-bottom: 0.3vw;
}

/* last .comment-item remove border  */
.comment-item:last-child {
    border-bottom: none;
}

.comment-item:hover {
    background-color: #f5f5f5;
    cursor: pointer;
}

.comment-header {
    display: flex;
    margin-bottom: 0.5vw;
    align-items: baseline;
    flex-direction: row;
    flex-wrap: nowrap;
    align-content: center;
    justify-content: flex-start;
    gap: 0.2vw;

}

.comment-user {
    font-weight: bold;
    color: #27a295;
    font-size: 0.8vw;
    font-family: wl2;
}

.comment-date {
    font-size: 0.4vw;
    color: #666;
}

.comment-text {
    margin-bottom: 0.5vw;
    color: #333;
    font-size: 0.6vw;
    font-family: 'wl1';
}

.comment-action {
    font-size: 0.4vw;
    color: #999;
    cursor: pointer;
    transition: color 0.2s;
    background: #cfcfcf;
    width: min-content;
    padding: 0.1vw 0.4vw;
}
</style>
