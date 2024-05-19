const axios = require('axios');

const openaiApiUrl = 'https://api.openai.com/v1/chat/completions'; // Replace with the correct endpoint
const apiKey = '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'; // Replace with your actual API key

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