import React, { useState } from 'react';
import axios from 'axios';

// Add a simple inline style object to keep things clean
const styles = {
    container: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        backgroundColor: '#f0f4f8',
        fontFamily: "'Roboto', sans-serif",
        color: '#333',
        padding: '20px',
    },
    header: {
        fontSize: '2rem',
        fontWeight: 'bold',
        color: '#2c3e50',
        marginBottom: '20px',
    },
    form: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        width: '100%',
        maxWidth: '500px',
    },
    input: {
        width: '100%',
        padding: '12px 20px',
        marginBottom: '15px',
        fontSize: '16px',
        borderRadius: '8px',
        border: '1px solid #bdc3c7',
        boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.1)',
        outline: 'none',
        transition: 'all 0.3s ease',
    },
    button: {
        padding: '12px 20px',
        fontSize: '16px',
        fontWeight: 'bold',
        color: '#fff',
        backgroundColor: '#3498db',
        borderRadius: '8px',
        border: 'none',
        cursor: 'pointer',
        transition: 'all 0.3s ease',
    },
    buttonHover: {
        backgroundColor: '#2980b9',
    },
    response: {
        marginTop: '20px',
        padding: '15px',
        backgroundColor: '#ecf0f1',
        borderRadius: '8px',
        color: '#2c3e50',
        boxShadow: '0px 4px 10px rgba(0, 0, 0, 0.1)',
        width: '100%',
        maxWidth: '500px',
        fontSize: '1.1rem',
    },
};

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
            setMessage(''); // Clear input after submit
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    return (
        <div style={styles.container}>
            <h1 style={styles.header}>Poker Strategy Chatbot</h1>
            <form style={styles.form} onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Ask me anything about poker strategy"
                    required
                    style={styles.input}
                />
                <button
                    type="submit"
                    style={{
                        ...styles.button,
                        ...(message ? styles.buttonHover : {}),
                    }}
                >
                    Send
                </button>
            </form>
            {response && <div style={styles.response}>Response: {response}</div>}
        </div>
    );
}

export default App;
