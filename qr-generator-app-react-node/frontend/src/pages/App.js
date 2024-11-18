import React, { useState } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState('');
  const [qrCodeUrl, setQrCodeUrl] = useState('');

  const generateQRCode = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/qr/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data }),
      });

      const result = await response.json();
      if (response.ok) {
        setQrCodeUrl(`http://localhost:5000${result.url}`);
      } else {
        alert(result.message || 'Error generating QR Code');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <h1>QR Code Generator</h1>
      <input
        type="text"
        placeholder="Enter data"
        value={data}
        onChange={(e) => setData(e.target.value)}
      />
      <button onClick={generateQRCode}>Generate QR Code</button>
      {qrCodeUrl && (
        <div>
          <h3>Your QR Code:</h3>
          <img src={qrCodeUrl} alt="QR Code" />
        </div>
      )}
    </div>
  );
}

export default App;
