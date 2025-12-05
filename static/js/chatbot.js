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
        bubble.textContent = text;

        div.appendChild(bubble);
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
    }

    function getResponse(query) {
        query = query.toLowerCase();
        if (query.includes('weather')) return "The weather is currently sunny with a 10% chance of rain.";
        if (query.includes('loan')) return "You can request a loan from the Finance section. Interest is 12% p.a.";
        if (query.includes('market') || query.includes('price')) return "Maize is trading at KES 4,500. Check the Marketplace for more.";
        if (query.includes('pest') || query.includes('disease')) return "For pest issues, please report to your Extension Officer immediately via the Dashboard.";
        return "I'm not sure about that. Try asking about weather, loans, or market prices.";
    }

    function handleSend() {
        const text = input.value.trim();
        if (text) {
            addMessage('You', text, true);
            input.value = '';
            setTimeout(() => {
                const response = getResponse(text);
                addMessage('AI', response);
            }, 500);
        }
    }

    send.addEventListener('click', handleSend);
    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSend();
    });
});
