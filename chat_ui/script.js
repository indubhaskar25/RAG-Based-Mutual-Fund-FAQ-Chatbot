// DOM Elements
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const chatMessages = document.getElementById('chatMessages');
const newChatBtn = document.querySelector('.new-chat-btn');
const clearChatsBtn = document.querySelector('.clear-chats-btn');
const historyItems = document.querySelectorAll('.history-item');

// Auto-resize textarea
messageInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 200) + 'px';
});

// Send message on Enter key (Shift+Enter for new line)
messageInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Send button click
sendBtn.addEventListener('click', sendMessage);

// New chat button
newChatBtn.addEventListener('click', function() {
    // Clear current chat messages
    chatMessages.innerHTML = `
        <div class="message assistant">
            <div class="message-avatar">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <path d="M12 16v-4"></path>
                    <path d="M12 8h.01"></path>
                </svg>
            </div>
            <div class="message-content">
                <p>Hello! I'm your RAG-based Mutual Fund FAQ assistant. I can help you with questions about mutual funds, investment strategies, and financial planning. What would you like to know?</p>
            </div>
        </div>
    `;
    
    // Remove active class from history items
    historyItems.forEach(item => item.classList.remove('active'));
});

// Clear all chats
clearChatsBtn.addEventListener('click', function() {
    if (confirm('Are you sure you want to clear all chat history?')) {
        // Clear chat history
        const historySections = document.querySelectorAll('.history-section');
        historySections.forEach(section => {
            const items = section.querySelectorAll('.history-item');
            items.forEach(item => item.remove());
        });
        
        // Clear current chat
        chatMessages.innerHTML = `
            <div class="message assistant">
                <div class="message-avatar">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <path d="M12 16v-4"></path>
                        <path d="M12 8h.01"></path>
                    </svg>
                </div>
                <div class="message-content">
                    <p>Hello! I'm your RAG-based Mutual Fund FAQ assistant. I can help you with questions about mutual funds, investment strategies, and financial planning. What would you like to know?</p>
                </div>
            </div>
        `;
    }
});

// History item click
historyItems.forEach(item => {
    item.addEventListener('click', function() {
        // Remove active class from all items
        historyItems.forEach(i => i.classList.remove('active'));
        // Add active class to clicked item
        this.classList.add('active');
        
        // In a real app, this would load the chat history
        // For demo, just show a loading state
        const chatText = this.querySelector('span').textContent;
        chatMessages.innerHTML = `
            <div class="message assistant">
                <div class="message-avatar">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle>
                        <path d="M12 16v-4"></path>
                        <path d="M12 8h.01"></path>
                    </svg>
                </div>
                <div class="message-content">
                    <p>Loading chat: "${chatText}"...</p>
                </div>
            </div>
        `;
    });
});

// Send message function
function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    // Add user message
    addMessage(message, 'user');
    
    // Clear input
    messageInput.value = '';
    messageInput.style.height = 'auto';
    
    // Generate contextual response based on message content
    setTimeout(() => {
        const response = generateContextualResponse(message);
        addMessage(response, 'assistant');
    }, 1000);
}

// Add message to chat
function addMessage(content, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    const avatarSvg = type === 'assistant' 
        ? `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <path d="M12 16v-4"></path>
            <path d="M12 8h.01"></path>
           </svg>`
        : `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
           </svg>`;
    
    // Convert markdown-style formatting to HTML
    const formattedContent = content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            ${avatarSvg}
        </div>
        <div class="message-content">
            <p>${formattedContent}</p>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Generate contextual response based on message content
function generateContextualResponse(message) {
    const lowerMessage = message.toLowerCase();
    
    // ICICI funds specific responses
    if (lowerMessage.includes('icici')) {
        return `Based on ICICI Prudential Mutual Fund offerings, here are some popular investment options:

**ICICI Prudential Bluechip Fund:** A large-cap equity fund investing in established companies with strong market positions. Suitable for long-term wealth creation with moderate risk.

**ICICI Prudential Balanced Advantage Fund:** A hybrid fund that dynamically allocates between equity and debt based on market valuations. Good for investors seeking balanced growth with lower volatility.

**ICICI Prudential Flexi Cap Fund:** Invests across market caps (large, mid, and small) with flexibility to adapt to market conditions. Suitable for aggressive investors with long-term horizons.

**Key Factors to Consider:**
- **Risk Profile:** Assess your risk tolerance before investing
- **Investment Horizon:** Equity funds require 5+ years for optimal returns
- **Expense Ratio:** ICICI funds typically have competitive expense ratios
- **Past Performance:** Review 3-5 year performance history
- **Fund Manager:** Consider the fund manager's track record

Would you like more details about any specific ICICI fund or investment strategy?`;
    }
    
    // General mutual fund responses
    if (lowerMessage.includes('invest') || lowerMessage.includes('fund')) {
        return `When considering mutual fund investments, here are the key factors to evaluate:

**1. Investment Objective:** Define your goal - wealth creation, regular income, or capital preservation

**2. Risk Tolerance:** 
- Low Risk: Debt funds, liquid funds
- Moderate Risk: Hybrid funds, balanced funds
- High Risk: Equity funds, sector funds

**3. Investment Horizon:**
- Short-term (<3 years): Debt funds, liquid funds
- Medium-term (3-5 years): Balanced funds, hybrid funds
- Long-term (5+ years): Equity funds, flexi-cap funds

**4. Fund Performance:** Look at consistent performance over 3-5 years, not just recent returns

**5. Expense Ratio:** Lower expense ratios (under 1% for equity, under 0.5% for debt) are preferable

**6. Fund Manager Experience:** Experienced managers with proven track records

**7. Asset Under Management (AUM):** Funds with adequate AUM (₹500+ crore) generally have better stability

Would you like specific fund recommendations based on your risk profile and investment goals?`;
    }
    
    // Default response
    return `I understand your question. As a RAG-based Mutual Fund FAQ assistant, I can help you with:

- **Fund Analysis:** Detailed information about specific mutual funds
- **Investment Strategies:** SIP vs Lumpsum, asset allocation, portfolio rebalancing
- **Risk Assessment:** Understanding different risk levels and suitable fund categories
- **Tax Implications:** Tax benefits, capital gains, and holding periods
- **Performance Comparison:** Comparing funds across categories and time periods

Please ask a specific question about mutual funds, and I'll provide detailed, factual information from our knowledge base. For personalized investment advice, please consult a SEBI-registered financial advisor.`;
}

// Scroll to bottom on load
chatMessages.scrollTop = chatMessages.scrollHeight;
