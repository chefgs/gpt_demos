
async function generateIdea() {
    const prompt = document.getElementById('ideaInput').value;
    const responseElement = document.getElementById('ideaOutput');
    responseElement.innerText = 'Generating...';

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt }),
        });

        const data = await response.json();
        if (data.success) {
            responseElement.innerText = data.choices[0].text;
        } else {
            responseElement.innerText = 'Failed to generate idea. Please try again.';
        }
    } catch (error) {
        console.error('Error:', error);
        responseElement.innerText = 'An error occurred. Please try again.';
    }
}
