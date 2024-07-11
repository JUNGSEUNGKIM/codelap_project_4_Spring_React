import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ChatWindow from "./ChatWindow";
import annyang from 'annyang';

const ChatBotPage = (props) => {
    const [question, setQuestion] = useState('');
    const [chatHistory, setChatHistory] = useState('');
    const [isFetching, setIsFetching] = useState(false);
    const [dots, setDots] = useState('');
    const [ttsEnabled, setTtsEnabled] = useState(false);

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

    function textToSpeech(message){
        const speech = new SpeechSynthesisUtterance();
        speech.text=message;
        window.speechSynthesis.speak(speech);
    }

    async function handleSubmit(){
        // event.preventDefault();
        if (question.trim()) {
            setIsFetching(true);
            setChatHistory(prev => `${prev}\n상담자: ${question}`);
            try {
                const response = await axios.post('http://localhost:5000/ere', { content: question }, { withCredentials: true });
                if (response.data.status === 'success') {
                    setChatHistory(prev => `${prev}\n챗봇: ${response.data.answer}`);
                    if(ttsEnabled) {
                        textToSpeech(response.data.answer)
                    }
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
    // useEffect(async ()=>{
    //     await handleSubmit()
    // }, [question])

    const startSpeechRecognition = () => {
        if (annyang) {
            annyang.setLanguage('ko-KR');
            annyang.addCommands({
                '*query': function (query) {
                    const resultWithoutSpaces = query.replace(/\s/g, '');
                    console.log(resultWithoutSpaces);
                    setQuestion(resultWithoutSpaces);

                }
            });

            annyang.start();

        }

    };

    const stopSpeechRecognition = async () => {
        if (annyang) {
            annyang.abort();
            await handleSubmit();
        }
    };

    const toggleChat = () => {
        setShowChat(!showChat);
    };

    const [showChat, setShowChat] = useState(false);
    const [fullScreen, setFullScreen] = useState(false);

    const openFullScreen = () => {
        setFullScreen(true);
    };

    const closeFullScreen = () => {
        setFullScreen(false);
    };

    const handleToggleTTS = () => {
        setTtsEnabled(!ttsEnabled); // TTS 상태를 토글하는 함수
    };



    return (
        <div className="App">
            <div className="chat-icon" onClick={toggleChat}
                 style={{ zIndex: '999', position: 'fixed', bottom: '20px', right: '20px', cursor: 'pointer' }}>
                <img src="assets/img/chatbot.jpg" alt="Chat Icon" width="50" height="50" />
            </div>
            <div className="chat-window" style={{
                cursor: 'pointer',
                position: 'fixed',
                bottom: '0',
                marginBottom: '5%',
                paddingBottom: '3%',
                marginRight:'1%',
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
                    width: '100%',
                    padding: '10px',
                    backgroundColor: '#ff0000',
                    color: '#fff',
                    border: 'none',
                    cursor: 'pointer'
                }}>X
                </button>
                <h4>에리허브(EreHub) 챗봇</h4>
                <textarea style={{width:"100%",resize: "none",overflowY: "scroll",
                    scrollBehavior: "smooth"}}
                    value={isFetching ? `응답중${dots}` : chatHistory}
                    rows="10"
                    cols="50"
                    readOnly

                />

                    <textarea style={{width:"100%",resize: "none"}}
                        value={question}
                        onChange={handleInputChange}
                        placeholder="상담 내용을 여기에 입력하세요."
                        rows="4"
                        cols="50"

                    />
                    <br />
                    <div style={{display:"flex", justifyContent: 'center'}}>
                    <button style={{ margin: "0% 1%", padding: "0 2%" }} onClick={handleSubmit}>보내기</button>
                    <button style={{ margin: "0% 1%", padding: "0 2%" }} onClick={startSpeechRecognition}>음성 입력 시작</button>
                    <button style={{ margin: "0% 1%", padding: "0 2%" }} onClick={stopSpeechRecognition }>음성 입력 종료</button>
                    </div>
                <div>
                    <div style={{ display: "block", unicodeBidi: "isolate" }}>
                        <label style={{
                            display: "inline-block",
                            maxWidth: "100%",
                            marginBottom: "5px",
                            fontWeight: "700",
                            boxSizing: "border-box"
                        }}>TTS On/Off :</label>
                        <input style={{ margin: "10%", lineHeight: "normal" }} type={"checkbox"} checked={ttsEnabled}
                               onChange={handleToggleTTS}/>
                    </div>
                </div>
            </div>
            {fullScreen && <ChatWindow onClose={closeFullScreen} />}
        </div>
    );
};

export default ChatBotPage;
