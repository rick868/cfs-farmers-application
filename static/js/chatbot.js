document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('chatbot-toggle');
    const window = document.getElementById('chatbot-window');
    const close = document.getElementById('chatbot-close');
    const input = document.getElementById('chatbot-input');
    const send = document.getElementById('chatbot-send');
    const messages = document.getElementById('chatbot-messages');

    toggle.addEventListener('click', () => window.style.display = 'flex');
    close.addEventListener('click', () => window.style.display = 'none');

    function addMessage(sender, text, isUser = false) {
        const div = document.createElement('div');
        div.style.marginBottom = '0.5rem';
        div.style.textAlign = isUser ? 'right' : 'left';

        const bubble = document.createElement('span');
        bubble.style.display = 'inline-block';
        bubble.style.padding = '0.5rem 0.8rem';
        bubble.style.borderRadius = '12px';
        bubble.style.background = isUser ? '#E8F5E9' : '#fff';
        bubble.style.border = isUser ? 'none' : '1px solid #eee';
        // Allow rendering HTML for bolding/formatting
        bubble.innerHTML = text;

        div.appendChild(bubble);
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
    }

    async function handleSend() {
        const text = input.value.trim();
        if (text) {
            addMessage('You', text, true);
            input.value = '';

            // Loading state
            const loadingDiv = document.createElement('div');
            loadingDiv.id = 'ai-loading';
            loadingDiv.style.textAlign = 'left';
            loadingDiv.innerHTML = '<span style="background:#fff; border:1px solid #eee; padding:0.5rem; border-radius:12px; color:#888;">Typing...</span>';
            messages.appendChild(loadingDiv);
            messages.scrollTop = messages.scrollHeight;

            try {
                const response = await fetch('/core/api/chat/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: text })
                });

                const data = await response.json();

                // Remove loading
                const loader = document.getElementById('ai-loading');
                if (loader) loader.remove();

                addMessage('AI', data.response);

            } catch (error) {
                console.error('Error:', error);

                // Remove loading
                const loader = document.getElementById('ai-loading');
                if (loader) loader.remove();

                addMessage('AI', "Sorry, I couldn't reach the server. Please check your connection.");
            }
        }
    }

    send.addEventListener('click', handleSend);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
    });
});
