const axios = require('axios');

const openaiApiUrl = 'https://api.openai.com/v1/chat/completions'; // Replace with the correct endpoint
const apiKey = ''; // Replace with your actual API key or add it in the ENV var

axios.post(openaiApiUrl, {
  prompt: "Translate the following English text to French: 'Hello, how are you?'",
  max_tokens: 60,
}, {
  headers: {
    'Authorization': `Bearer ${apiKey}`,
  }
})
.then(response => {
  console.log(response.data);
})
.catch(error => {
  console.error('Error making request:', error.message);
});