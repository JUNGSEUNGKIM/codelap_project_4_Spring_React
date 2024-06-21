import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ChatWindow from "./ChatWindow";


function ChatBotPage(props) {
    const [question, setQuestion] = useState('');
    const [chatHistory, setChatHistory] = useState('');
    const [isFetching, setIsFetching] = useState(false);
    const [dots, setDots] = useState('');

    useEffect(() => {
        if (isFetching) {
            const interval = setInterval(() => {
                setDots(dots => dots.length < 10 ? dots + '.' : '');
            }, 500);
            return () => clearInterval(interval);
        }
    }, [isFetching]);

    const handleInputChange = (event) => {
        setQuestion(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (question.trim()) {
            setIsFetching(true);
            setChatHistory(prev => `${prev}\n상담자: ${question}`);
            // alert("reponse check ::::: "+question)
            try {
                const response = await axios.post('http://localhost:5000/ere', { content: question },{withCredentials: true} );
                // alert("reponse check :::::" + response.data)
                if (response.data.status === 'success') {
                    setChatHistory(prev => `${prev}\n쳇봇: ${response.data.answer}`);
                } else {
                    alert('Error: ' + response.data.message);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                setIsFetching(false);
            }
            setQuestion('');
        }
    };

    const [showChat, setShowChat] = useState(false);
    const [fullScreen, setFullScreen] = useState(false);

    const toggleChat = () => {
        setShowChat(!showChat);
        console.log(showChat)
    };

    const openFullScreen = () => {
        setFullScreen(true);
    };

    const closeFullScreen = () => {
        setFullScreen(false);
    };

    return (
        <div className="App">

            <div
                className="chat-icon"
                onClick={() => {
                    toggleChat()
                }}

                style={{zIndex: '999', position: 'fixed', bottom: '20px', right: '20px', cursor: 'pointer'}}
            >
                <img src="assets/img/chatbot.jpg" alt="Chat Icon" width="50" height="50"/>
            </div>
            <div className="chat-window" style={{
                cursor: 'pointer',
                position: 'fixed',
                bottom: '0',
                marginBottom: '5%',
                paddingBottom: '3%',
                right: '0',
                width: '300px',
                height: '500px',
                backgroundColor: '#ffffff',
                border: '1px solid #ccc',
                zIndex: '999',
                boxShadow: '0 0 10px rgba(0, 0, 0, 0.1)',
                display: `${showChat ? 'block' : 'none'}`
            }}>
                <button onClick={toggleChat} style={{
                    // position: 'fixed',
                    // bottom: '0.2',
                    width: '100%',
                    padding: '10px',
                    backgroundColor: '#ff0000',
                    color: '#fff',
                    border: 'none',
                    cursor: 'pointer'
                }}>X
                </button>


                <h4>에리허브(EreHub) 챗봇</h4>
                <textarea
                    value={isFetching ? `응답중${dots}` : chatHistory}
                    rows="14"
                    cols="50"
                    readOnly
                />
                <form onSubmit={handleSubmit}>
                <textarea
                    value={question}
                    onChange={handleInputChange}
                    placeholder="상담 내용을 여기에 입력하세요."
                    rows="4"
                    cols="50"
                />
                    <br/>
                    <button type="submit">보내기</button>
                </form>
            </div>
            {fullScreen && <ChatWindow onClose={closeFullScreen}/>}
        </div>
    )
}

export default ChatBotPage;