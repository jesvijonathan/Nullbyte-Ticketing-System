<template>
    <div v-if="pr" class="github-pr-container">
      <div v-if="loading" class="github-loading">Loading...</div>
      <div v-else-if="error" class="github-error">{{ error }}</div>
      <div v-else class="github-pr-details">
        
        <h1 class="github-pr-title"> {{ pullRequest.title }} [<span :class="{'open-state': pullRequest.state === 'open', 'closed-state': pullRequest.state === 'closed'}">{{ pullRequest.state }}</span>]</h1>
        <p v-if="pullRequest.user && pullRequest.user.login" class="github-pr-user">
          <strong>Created by:</strong> {{ pullRequest.user.login }}
        </p>
        <p class="github-pr-user">
          <strong>Created at:</strong> {{ new Date(pullRequest.created_at).toLocaleString() }}
        </p>
        <p class="github-pr-files-title">Body:</p>
        <pre class="github-pr-body">{{ pullRequest.body }}</pre>
        <h3 class="github-pr-files-title">Files Changed:</h3>
        <ul class="github-pr-files-list">
          <li v-for="file in pullRequest.files" :key="file.filename" class="github-pr-file-item">
            {{ file.filename }} ({{ file.status }})
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  
  const props = defineProps({
    pr: {
      type: String
    }
  });
  
  const pr_def = ref("");
  
  const owner = ref('');
  const repo = ref('');
  const pullNumber = ref('');
  const loading = ref(false);
  const error = ref(null);
  const pullRequest = ref({});
  
  function ParseGit() {
    const url = pr_def.value;
    const urlParts = url.split('/');
    owner.value = urlParts[3];
    repo.value = urlParts[4];
    pullNumber.value = urlParts[6];
  }
  
  onMounted(async () => {
    loading.value = true;
  
    pr_def.value = props.pr;
    ParseGit();
  
    try {
      const response = await axios.get(`https://api.github.com/repos/${owner.value}/${repo.value}/pulls/${pullNumber.value}`);
      pullRequest.value = response.data;
      const filesResponse = await axios.get(`https://api.github.com/repos/${owner.value}/${repo.value}/pulls/${pullNumber.value}/files`);
      pullRequest.value.files = filesResponse.data;
    } catch (err) {
      error.value = 'Failed to load pull request details: ' + err.message;
    } finally {
      loading.value = false;
    }
  });
  </script>
  
  <style scoped>
  .github-pr-container {
    /* background-color: #f6f8fa; */
    border: 0.1vw solid #d1d5da;
    padding: 0.7vw;
    border-radius: 0.4vw;
    font-family: wl1;
    /* width: fit-content; */
    width: 42vw;
    margin: 2vw auto;
    margin-top:1vw;
    /* border-right : none;
    border-left : none;  */
  }
  .github-pr-container:hover .github-pr-details{
    background-color: #dfdfdf2e;
  }

  .github-pr-container *{
    font-family: "Source Code Pro", monospace;
    font-optical-sizing: auto;
    font-style: normal;
  }
  
  .github-pr-title {
    font-size: 1vw;
    font-weight: 600;
    margin-bottom: 1.8vw;
    color: #000000;
    font-weight: 600;
    font-family: wl2;
  }
  .github-pr-title:hover{
    cursor: pointer;
    text-decoration: underline;
  }
  
  .github-loading,
  .github-error {
    font-size: 1vw;
    color: #d73a49;
  }
  
  .github-pr-details {
    padding: 00.8vw;
    padding-top: 0vw;
    background-color: #ffffff;
    border-radius: 0.2vw;
    padding-top: 1vw;
    margin-top: 0vw;
  }
  
  .github-pr-user,
  .github-pr-date,
  .github-pr-state {
    margin: 0.5vw 0;
    font-size: 0.8vw;
    color: #586069;
  }
  
  .github-pr-user strong{
    font-weight: 600;
    font-family: wl3;
  }
  .open-state {
    color: #28a745;
  }
  
  .closed-state {
    color: #d73a49;
  }
  
  /* .github-pr-body-label{
    font-size: 1vw;
    font-weight: 600;
    color: #24292e;
  } */
/*   
  .github-pr-body {
    margin-top: 1vw;
    background-color: #ececec6b;
    padding: 1vw;
    font-size: 0.9vw;
    border-radius: 0.2vw;
    white-space: pre-wrap;
    word-wrap: break-word;
    font-size: 0.8vw;
    padding-left: 3vw;
  } */
  
  .github-pr-files-title, .github-pr-body-label * {
    margin-top: 1vw;
    font-size: 0.9vw;
    font-weight: 600;
    color: #24292e;
    margin-top: 2vw;
    font-weight: 600;
    font-family: wl3;
  }
  
  .github-pr-files-list, .github-pr-body {
    margin-top: 0.5vw;
    white-space: pre-wrap;
    word-wrap: break-word;
    font-size: 0.7vw;
    list-style-type: none;
    padding-left: 0;
    background-color: #ececec6b;
    border-radius: 0.2vw;
    padding: 2vw;
    padding: 1vw;
  }
  .github-pr-file-item:hover{
    background-color: #cccccc64;
    cursor: pointer;
  }
  .github-pr-file-item {
    padding: 0.1vw 0.3vw;
    border-radius: 0vw;
    font-size: 0.7vw;
  }
  </style>
  