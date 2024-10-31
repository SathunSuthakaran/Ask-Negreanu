import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [message, setMessage] = useState('');
    const [response, setResponse] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post('http://127.0.0.1:5000/api/message', {
                message: message,
            });
            const answer = res.data.response.split("Answer:")[1]?.trim();
            setResponse(answer);
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    return (
        <div>
            <h1>Poker Chatbot</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Ask me anything"
                    required
                />
                <button type="submit">Send</button>
            </form>
            {response && <p>Response: {response}</p>}
        </div>
    );
}

export default App;
