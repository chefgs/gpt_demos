
require('dotenv').config();
const express = require('express');
const axios = require('axios');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static('public'));
app.use(express.json());

app.post('/generate', async (req, res) => {
    const prompt = req.body.prompt;
    try {
        const response = await axios.post(
            'https://api.openai.com/v1/completions',
            {
                model: "gpt-4", // Updated to use a hypothetical GPT-4 model
                prompt: `Generate an app idea: ${prompt}`,
                temperature: 0.7,
                max_tokens: 256,
                top_p: 1,
                frequency_penalty: 0,
                presence_penalty: 0,
            },
            { headers: { Authorization: `Bearer ${process.env.OPENAI_API_KEY}` } }
        );
        res.json({ success: true, response: response.data.choices[0].text });
    } catch (error) {
        console.error('OpenAI API Error:', error);
        res.status(500).json({ success: false, message: 'Error generating app idea' });
    }
});

app.listen(PORT, () => console.log(`Server listening on port ${PORT}`));
