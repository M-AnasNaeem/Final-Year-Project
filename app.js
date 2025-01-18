class ChatBot {
    constructor() {
        this.state = {
            isOpen: false,
            messages: [],
            isTyping: false
        };
        
        // DOM Elements
        this.container = document.getElementById('chat-container');
        this.toggle = document.getElementById('chat-toggle');
        this.window = document.getElementById('chat-window');
        this.messagesContainer = document.getElementById('chat-messages');
        this.form = document.getElementById('chat-form');
        this.input = document.getElementById('chat-input');
        
        this.selectedLanguage = null;
        
        this.init();
    }

    init() {
        // Add language button listeners
        document.querySelectorAll('.language-btn').forEach(button => {
            button.addEventListener('click', (e) => this.handleLanguageSelection(e));
        });
        
        // Event Listeners
        this.toggle.addEventListener('click', () => this.toggleChat());
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        
        // Load chat history
        this.loadHistory();
    }

    toggleChat() {
        this.state.isOpen = !this.state.isOpen;
        this.window.classList.toggle('active');
        this.window.setAttribute('aria-hidden', !this.state.isOpen);
        
        if (this.state.isOpen) {
            this.input.focus();
        }
    }

    async handleSubmit(e) {
        e.preventDefault();
        const message = this.input.value.trim();
        
        if (!message) return;
        
        // Add user message
        this.addMessage({ text: message, type: 'user' });
        this.input.value = '';
        
        // Show typing indicator
        this.setTyping(true);
        
        try {
           
            const response = await this.processMessage(message);
            
            // Add bot response
            this.addMessage({ text: response, type: 'bot' });
        } catch (error) {
            this.addMessage({ 
                text: "I apologize, but I encountered an error. Please try again.",
                type: 'bot'
            });
        } finally {
            this.setTyping(false);
        }
    }

    async processMessage(message) {
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    message,
                    language: this.selectedLanguage  // Add the selected language to each request
                })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            return data.response;
        } catch (error) {
            console.error('Error processing message:', error);
            throw error;
        }
    }

    addMessage({ text, type }) {
        const message = { text, type, timestamp: new Date().toISOString() };
        this.state.messages.push(message);
        
        const messageEl = document.createElement('div');
        messageEl.className = `message ${type}`;
        messageEl.textContent = text;
        
        this.messagesContainer.appendChild(messageEl);
        this.scrollToBottom();
        this.saveHistory();
    }

    setTyping(isTyping) {
        this.state.isTyping = isTyping;
        const existingLoader = this.messagesContainer.querySelector('.loading-container');
        
        if (isTyping) {
            if (!existingLoader) {
                const loadingContainer = document.createElement('div');
                loadingContainer.className = 'message bot loading-container';
                
                const loadingBar = document.createElement('div');
                loadingBar.className = 'loading-bar';
                
                loadingContainer.appendChild(loadingBar);
                this.messagesContainer.appendChild(loadingContainer);
            }
        } else {
            if (existingLoader) {
                existingLoader.remove();
            }
        }
        this.scrollToBottom();
    }

    scrollToBottom() {
        requestAnimationFrame(() => {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        });
    }

    saveHistory() {
        try {
            sessionStorage.setItem('chatHistory', JSON.stringify(this.state.messages));
        } catch (e) {
            console.warn('Failed to save chat history:', e);
        }
    }

    loadHistory() {
        try {
            const history = sessionStorage.getItem('chatHistory');
            if (history) {
                const messages = JSON.parse(history);
                messages.forEach(message => this.addMessage(message));
            }
        } catch (e) {
            console.warn('Failed to load chat history:', e);
        }
    }

    handleLanguageSelection(e) {
        const selectedLang = e.target.dataset.lang;
        this.selectedLanguage = selectedLang;
        
        // Remove language selector
        const languageSelector = document.getElementById('language-selector');
        languageSelector.remove();
        
        // Send language preference to backend and get translated welcome message
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                message: "GREETING",
                language: selectedLang 
            })
        })
        .then(response => response.json())
        .then(data => {
            this.addMessage({
                text: data.response,
                type: 'bot'
            });
            // Add option buttons after welcome message
            this.addOptionButtons();
        });
    }

    addOptionButtons() {
        const optionsContainer = document.createElement('div');
        optionsContainer.className = 'message bot option-buttons';
        
        const options = [
            'Where is my car located?',
            'What is my loading schedule?',
            'What is the status of my payment?',
            'What are the details of my car payment?',
            'What is the arrival information?'
        ];

        // If language is not English, translate the options
        if (this.selectedLanguage !== 'en') {
            fetch('/api/translate-options', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    options: options,
                    language: this.selectedLanguage
                })
            })
            .then(response => response.json())
            .then(data => {
                this.createOptionButtons(optionsContainer, data.translated_options);
            });
        } else {
            this.createOptionButtons(optionsContainer, options);
        }

        this.messagesContainer.appendChild(optionsContainer);
        this.scrollToBottom();
    }

    createOptionButtons(container, options) {
        options.forEach(option => {
            const button = document.createElement('button');
            button.className = 'option-btn';
            button.textContent = option;
            button.addEventListener('click', () => {
                this.handleOptionClick(option);
            });
            container.appendChild(button);
        });
    }

    handleOptionClick(option) {
        
        this.input.value = option;
        this.form.dispatchEvent(new Event('submit'));
    }
}


document.addEventListener('DOMContentLoaded', () => {
    window.chatbot = new ChatBot();
});
