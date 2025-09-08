// Chat Application State
let sessionId = null;
let isProcessing = false;
let messageCount = 0;

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const loadingIndicator = document.getElementById('loadingIndicator');
const sidebarToggle = document.getElementById('sidebarToggle');
const chatSidebar = document.getElementById('chatSidebar');

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeChat();
    setupEventListeners();
    setupQuickActions();
});

// Initialize chat session
async function initializeChat() {
    try {
        showLoading('Initializing AI Agent...');
        
        const response = await fetch('/api/initialize', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: `web_user_${Date.now()}`
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            sessionId = data.session_id;
            hideLoading();
            addSystemMessage('AI-AH Terraform Engineer is ready! 🚀');
        } else {
            throw new Error(data.error || 'Failed to initialize agent');
        }
    } catch (error) {
        console.error('Initialization error:', error);
        hideLoading();
        addSystemMessage('❌ Failed to initialize agent. Please refresh the page.', 'error');
    }
}

// Setup event listeners
function setupEventListeners() {
    // Send message on Enter key
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Send button click
    sendButton.addEventListener('click', sendMessage);
    
    // Auto-resize textarea
    messageInput.addEventListener('input', autoResizeTextarea);
    
    // Sidebar toggle
    sidebarToggle.addEventListener('click', toggleSidebar);
    
    // Action buttons
    document.getElementById('clearChat').addEventListener('click', clearChat);
    document.getElementById('exportChat').addEventListener('click', exportChat);
    document.getElementById('workspaceStatus').addEventListener('click', checkWorkspace);

    // Requirements Form Button
    document.getElementById('requirementsFormBtn').addEventListener('click', function() {
        showRequirementsModal();
    });
}

// Setup quick action buttons
function setupQuickActions() {
    const quickActions = document.querySelectorAll('.quick-action');
    
    quickActions.forEach(button => {
        button.addEventListener('click', function() {
            const action = this.dataset.action;
            handleQuickAction(action);
        });
    });
}

// Handle quick actions
function handleQuickAction(action) {
    let message = '';
    
    switch(action) {
        case 'serverless':
            message = 'Create a serverless architecture with Lambda and DynamoDB';
            break;
        case 'microservices':
            message = 'Design a microservices infrastructure with API Gateway and containers';
            break;
        case 'three-tier':
            message = 'Create a 3-tier web application infrastructure with load balancer and RDS';
            break;
        case 'container':
            message = 'Design a container-based infrastructure with ECS and ALB';
            break;
        case 'aws':
            message = 'Show me AWS infrastructure best practices and cost optimization';
            break;
        case 'azure':
            message = 'Help me design Azure infrastructure for a web application';
            break;
        case 'gcp':
            message = 'Create Google Cloud infrastructure with Cloud Run and Firestore';
            break;
        case 'init':
            message = 'Initialize Terraform workspace';
            break;
        case 'plan':
            message = 'Run terraform plan to preview changes';
            break;
        case 'apply':
            message = 'Apply Terraform changes to deploy infrastructure';
            break;
        case 'destroy':
            message = 'Destroy infrastructure (use with caution)';
            break;
        case 'workspace':
            checkWorkspace();
            return;
        case 'stats':
            showSessionStats();
            return;
        case 'help':
            showHelp();
            return;
        default:
            message = `Help me with ${action}`;
    }
    
    messageInput.value = message;
    sendMessage();
}

// Send message to the agent
async function sendMessage(message = null) {
    const messageInput = document.getElementById('messageInput');
    const messageText = message || messageInput.value.trim();
    
    if (!messageText) return;
    
    // Check if this is an infrastructure creation request
    if (isInfrastructureRequest(messageText)) {
        showRequirementsModal();
        return;
    }
    
    // Add user message to chat
    addUserMessage(messageText);
    messageInput.value = '';
    autoResizeTextarea();
    
    // Show loading indicator
    showLoading('AI is thinking...');
    isProcessing = true;
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: messageText,
                session_id: sessionId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Add AI response to chat
            addAgentMessage(data.response);
        } else {
            addSystemMessage(`❌ Error: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Chat error:', error);
        addSystemMessage('❌ Failed to send message. Please try again.', 'error');
    } finally {
        hideLoading();
        isProcessing = false;
    }
}

// Add user message to chat
function addUserMessage(message) {
    messageCount++;
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-header">
                <span class="message-avatar">👤</span>
                <span class="message-name">You</span>
                <span class="message-time">${getCurrentTime()}</span>
            </div>
            <div class="message-text">${escapeHtml(message)}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Add agent message to chat
function addAgentMessage(message, pluginsUsed = [], confidence = 0) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message agent-message';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const messageHeader = document.createElement('div');
    messageHeader.className = 'message-header';
    
    const avatar = document.createElement('span');
    avatar.className = 'message-avatar';
    avatar.textContent = '🤖';
    
    const name = document.createElement('span');
    name.className = 'message-name';
    name.textContent = 'AI-AH Terraform Engineer';
    
    const time = document.createElement('span');
    time.className = 'message-time';
    time.textContent = getCurrentTime();
    
    messageHeader.appendChild(avatar);
    messageHeader.appendChild(name);
    messageHeader.appendChild(time);
    
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.innerHTML = formatMessage(message);
    
    messageContent.appendChild(messageHeader);
    messageContent.appendChild(messageText);
    
    // Add action buttons if this is a requirements collection message
    if (message.includes('❓ To proceed, I need some additional information:') || 
        message.includes('💡 Answer these questions to get started:')) {
        const actionButtons = createRequirementsActionButtons();
        messageContent.appendChild(actionButtons);
    }
    
    // Add action buttons if this is a proceed message
    if (message.includes('💡 Next: I can now generate the complete Terraform code')) {
        const actionButtons = createCodeGenerationButtons();
        messageContent.appendChild(actionButtons);
    }
    
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Add system message to chat
function addSystemMessage(message, type = 'info') {
    messageCount++;
    const messageDiv = document.createElement('div');
    messageDiv.className = `message system-message ${type}`;
    
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-header">
                <span class="message-avatar">ℹ️</span>
                <span class="message-name">System</span>
                <span class="message-time">${getCurrentTime()}</span>
            </div>
            <div class="message-text">${escapeHtml(message)}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Format message content (handle markdown-like syntax)
function formatMessage(message) {
    // Convert **text** to <strong>text</strong>
    message = message.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert *text* to <em>text</em>
    message = message.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    // Convert `code` to <code>code</code>
    message = message.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Convert newlines to <br> tags
    message = message.replace(/\n/g, '<br>');
    
    return message;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Get current time
function getCurrentTime() {
    return new Date().toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

// Auto-resize textarea
function autoResizeTextarea() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
}

// Scroll chat to bottom
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Show loading indicator
function showLoading(message = 'AI is thinking...') {
    loadingIndicator.querySelector('span').textContent = message;
    loadingIndicator.classList.add('show');
}

// Hide loading indicator
function hideLoading() {
    loadingIndicator.classList.remove('show');
}

// Toggle sidebar
function toggleSidebar() {
    chatSidebar.classList.toggle('open');
    sidebarToggle.textContent = chatSidebar.classList.contains('open') ? '▶' : '◀';
}

// Clear chat
function clearChat() {
    if (confirm('Are you sure you want to clear the chat history?')) {
        chatMessages.innerHTML = '';
        addSystemMessage('Chat history cleared. 🗑️');
    }
}

// Export chat
function exportChat() {
    const messages = chatMessages.querySelectorAll('.message');
    let exportText = 'AI-AH Terraform Engineer Chat Export\n';
    exportText += '='.repeat(50) + '\n\n';
    
    messages.forEach(message => {
        const name = message.querySelector('.message-name').textContent;
        const text = message.querySelector('.message-text').textContent;
        const time = message.querySelector('.message-time').textContent;
        
        exportText += `[${time}] ${name}:\n${text}\n\n`;
    });
    
    const blob = new Blob([exportText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `terraform-chat-export-${new Date().toISOString().split('T')[0]}.txt`;
    a.click();
    URL.revokeObjectURL(url);
}

// Check workspace status
async function checkWorkspace() {
    try {
        showLoading('Checking workspace...');
        
        const response = await fetch('/api/status', { 
            method: 'GET' 
        });
        
        const data = await response.json();
        
        if (data.success) {
            let workspaceInfo = '📁 **System Status:**\n\n';
            workspaceInfo += `**Status:** ${data.status}\n`;
            workspaceInfo += `**Active Sessions:** ${data.active_sessions}\n`;
            workspaceInfo += `**Max Sessions:** ${data.max_sessions}\n`;
            workspaceInfo += `**Session Timeout:** ${data.session_timeout} seconds\n`;
            workspaceInfo += `**Cleanup Interval:** ${data.cleanup_interval} seconds\n`;
            workspaceInfo += `**Workspace Exists:** ${data.workspace_exists ? 'Yes' : 'No'}\n`;
            
            if (data.workspace_exists) {
                workspaceInfo += `**Workspace Size:** ${(data.workspace_size_bytes / 1024 / 1024).toFixed(2)} MB\n`;
            }
            
            addSystemMessage(workspaceInfo);
        } else {
            throw new Error(data.error || 'Failed to check system status');
        }
    } catch (error) {
        console.error('Status check error:', error);
        addSystemMessage('❌ Failed to check system status.', 'error');
    } finally {
        hideLoading();
    }
}

// Show session statistics
function showSessionStats() {
    const stats = `📊 **Session Statistics:**\n\n`;
    stats += `**Messages:** ${messageCount}\n`;
    stats += `**Session ID:** ${sessionId || 'Not initialized'}\n`;
    stats += `**Status:** ${isProcessing ? 'Processing...' : 'Ready'}\n`;
    
    addSystemMessage(stats);
}

// Show help
function showHelp() {
    const help = `📋 **Available Commands:**\n\n`;
    help += `**Quick Actions (Sidebar):**\n`;
    help += `• Infrastructure patterns (Serverless, Microservices, etc.)\n`;
    help += `• Cloud providers (AWS, Azure, GCP)\n`;
    help += `• Terraform operations (Init, Plan, Apply, Destroy)\n\n`;
    help += `**Chat Actions:**\n`;
    help += `• Clear chat history\n`;
    help += `• Export chat to file\n`;
    help += `• Check workspace status\n`;
    help += `• View session statistics\n\n`;
    help += `**Try asking:**\n`;
    help += `• "Create a serverless architecture with Lambda and DynamoDB"\n`;
    help += `• "Help me deploy this infrastructure step by step"\n`;
    help += `• "My Terraform apply is failing, help me troubleshoot"`;
    
    addSystemMessage(help);
}

// Handle window resize
window.addEventListener('resize', function() {
    if (window.innerWidth <= 768) {
        chatSidebar.classList.remove('open');
        sidebarToggle.textContent = '◀';
    }
});

// Focus input on page load
window.addEventListener('load', function() {
    messageInput.focus();
});

// Create requirements action buttons
function createRequirementsActionButtons() {
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'action-buttons';
    
    const answerButton = document.createElement('button');
    answerButton.className = 'action-button primary';
    answerButton.textContent = '📝 Answer Questions';
    answerButton.onclick = () => {
        messageInput.value = 'answer 1 medium';
        messageInput.focus();
    };
    
    const summaryButton = document.createElement('button');
    summaryButton.className = 'action-button secondary';
    summaryButton.textContent = '📋 Requirements Summary';
    summaryButton.onclick = () => {
        messageInput.value = 'requirements summary';
        messageInput.focus();
    };
    
    const defaultsButton = document.createElement('button');
    defaultsButton.className = 'action-button secondary';
    defaultsButton.textContent = '🚀 Proceed with Defaults';
    defaultsButton.onclick = () => {
        messageInput.value = 'proceed with defaults';
        messageInput.focus();
    };
    
    buttonContainer.appendChild(answerButton);
    buttonContainer.appendChild(summaryButton);
    buttonContainer.appendChild(defaultsButton);
    
    return buttonContainer;
}

// Create code generation action buttons
function createCodeGenerationButtons() {
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'action-buttons';
    
    const generateButton = document.createElement('button');
    generateButton.className = 'action-button primary';
    generateButton.textContent = '⚡ Generate Terraform Code';
    generateButton.onclick = () => {
        messageInput.value = 'generate the code';
        messageInput.focus();
    };
    
    const reviewButton = document.createElement('button');
    reviewButton.className = 'action-button secondary';
    reviewButton.textContent = '📋 Review Requirements';
    reviewButton.onclick = () => {
        messageInput.value = 'requirements summary';
        messageInput.focus();
    };
    
    const deployButton = document.createElement('button');
    deployButton.className = 'action-button secondary';
    deployButton.textContent = '🚀 Deploy Infrastructure';
    deployButton.onclick = () => {
        messageInput.value = 'deploy the infrastructure';
        messageInput.focus();
    };
    
    buttonContainer.appendChild(generateButton);
    buttonContainer.appendChild(reviewButton);
    buttonContainer.appendChild(deployButton);
    
    return buttonContainer;
}

// Requirements Collection Modal Functions
let currentTab = 0;
const tabs = ['basic', 'performance', 'security', 'cost', 'compliance', 'advanced'];

function showRequirementsModal() {
    document.getElementById('requirementsModal').style.display = 'block';
    document.body.style.overflow = 'hidden';
    resetForm();
    
    // Get the current chat message to analyze what's needed
    const userMessages = document.querySelectorAll('.message.user');
    let lastInfrastructureRequest = '';
    
    // Find the last infrastructure-related message
    for (let i = userMessages.length - 1; i >= 0; i--) {
        const message = userMessages[i].textContent || userMessages[i].innerText;
        if (isInfrastructureRequest(message)) {
            lastInfrastructureRequest = message;
            break;
        }
    }
    
    // Determine which tabs to show based on the request
    const requiredTabs = determineRequiredTabs(lastInfrastructureRequest);
    showOnlyRequiredTabs(requiredTabs);
    
    // Show the first available tab
    const firstTab = Object.keys(requiredTabs).find(tab => requiredTabs[tab]);
    if (firstTab) {
        showTab(firstTab);
    } else {
        showTab('basic');
    }
}

function closeRequirementsModal() {
    document.getElementById('requirementsModal').style.display = 'none';
    document.body.style.overflow = 'auto';
    resetForm();
}

function showTab(tabName) {
    // Hide all tab contents
    tabs.forEach(tab => {
        document.getElementById(tab).classList.remove('active');
        document.querySelector(`[onclick="showTab('${tab}')"]`).classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    document.querySelector(`[onclick="showTab('${tabName}')"]`).classList.add('active');
    
    // Update current tab index
    currentTab = tabs.indexOf(tabName);
    
    // Update progress bar
    updateProgress();
    
    // Update navigation buttons
    updateNavigationButtons();
}

function nextTab() {
    const visibleTabs = Array.from(document.querySelectorAll('.tab-button')).filter(btn => 
        btn.style.display !== 'none'
    );
    
    if (currentTab < visibleTabs.length - 1) {
        currentTab++;
        const tabName = visibleTabs[currentTab].getAttribute('onclick').match(/'([^']+)'/)[1];
        showTab(tabName);
    }
}

function previousTab() {
    if (currentTab > 0) {
        currentTab--;
        const visibleTabs = Array.from(document.querySelectorAll('.tab-button')).filter(btn => 
            btn.style.display !== 'none'
        );
        const tabName = visibleTabs[currentTab].getAttribute('onclick').match(/'([^']+)'/)[1];
        showTab(tabName);
    }
}

function updateProgress() {
    // Count only visible tabs
    const visibleTabs = Array.from(document.querySelectorAll('.tab-button')).filter(btn => 
        btn.style.display !== 'none'
    );
    
    const progress = ((currentTab + 1) / visibleTabs.length) * 100;
    document.getElementById('progressFill').style.width = progress + '%';
    document.getElementById('progressText').textContent = Math.round(progress) + '% Complete';
}

function updateNavigationButtons() {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    
    const visibleTabs = Array.from(document.querySelectorAll('.tab-button')).filter(btn => 
        btn.style.display !== 'none'
    );
    
    // Show/hide Previous button
    if (currentTab === 0) {
        prevBtn.style.display = 'none';
    } else {
        prevBtn.style.display = 'inline-block';
    }
    
    // Show/hide Next/Submit buttons
    if (currentTab === visibleTabs.length - 1) {
        nextBtn.style.display = 'none';
        submitBtn.style.display = 'inline-block';
    } else {
        nextBtn.style.display = 'inline-block';
        submitBtn.style.display = 'none';
    }
}

function resetForm() {
    document.getElementById('requirementsForm').reset();
    currentTab = 0;
    updateProgress();
    updateNavigationButtons();
}

function submitRequirements() {
    // Collect form data
    const formData = new FormData(document.getElementById('requirementsForm'));
    const requirements = {};
    
    // Convert FormData to object
    for (let [key, value] of formData.entries()) {
        if (requirements[key]) {
            // Handle multiple values (checkboxes)
            if (Array.isArray(requirements[key])) {
                requirements[key].push(value);
            } else {
                requirements[key] = [requirements[key], value];
            }
        } else {
            requirements[key] = value;
        }
    }
    
    // Validate required fields
    if (!requirements.projectName || !requirements.environment || !requirements.pattern) {
        alert('Please fill in all required fields (marked with *)');
        return;
    }
    
    // Close modal
    closeRequirementsModal();
    
    // Send requirements to chat
    const requirementsText = formatRequirementsForChat(requirements);
    sendMessage(requirementsText);
    
    // Show success message
    addSystemMessage('✅ Requirements submitted successfully! Processing your infrastructure request...', 'success');
}

function formatRequirementsForChat(requirements) {
    let text = `Create infrastructure with the following requirements:\n\n`;
    text += `**Project:** ${requirements.projectName}\n`;
    text += `**Environment:** ${requirements.environment}\n`;
    text += `**Pattern:** ${requirements.pattern}\n`;
    
    if (requirements.region) text += `**Region:** ${requirements.region}\n`;
    if (requirements.description) text += `**Description:** ${requirements.description}\n`;
    
    if (requirements.expectedUsers) text += `**Expected Users:** ${requirements.expectedUsers}\n`;
    if (requirements.responseTime) text += `**Response Time:** ${requirements.responseTime}\n`;
    if (requirements.availability) text += `**Availability:** ${requirements.availability}\n`;
    
    if (requirements.securityLevel) text += `**Security Level:** ${requirements.securityLevel}\n`;
    if (requirements.budgetRange) text += `**Budget:** ${requirements.budgetRange}\n`;
    if (requirements.industry) text += `**Industry:** ${requirements.industry}\n`;
    
    // Add selected checkboxes
    if (requirements.scaling) {
        const scalingArray = Array.isArray(requirements.scaling) ? requirements.scaling : [requirements.scaling];
        text += `**Scaling:** ${scalingArray.join(', ')}\n`;
    }
    
    if (requirements.compliance) {
        const complianceArray = Array.isArray(requirements.compliance) ? requirements.compliance : [requirements.compliance];
        text += `**Compliance:** ${complianceArray.join(', ')}\n`;
    }
    
    if (requirements.encryption) {
        const encryptionArray = Array.isArray(requirements.encryption) ? requirements.encryption : [requirements.encryption];
        text += `**Encryption:** ${encryptionArray.join(', ')}\n`;
    }
    
    if (requirements.additionalNotes) text += `**Additional Notes:** ${requirements.additionalNotes}\n`;
    
    return text;
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('requirementsModal');
    if (event.target === modal) {
        closeRequirementsModal();
    }
}

// Close modal with Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeRequirementsModal();
    }
});

function isInfrastructureRequest(message) {
    const infrastructureKeywords = [
        'create', 'build', 'design', 'deploy', 'set up', 'infrastructure',
        'serverless', 'microservices', 'architecture', 'vpc', 'lambda',
        'ecs', 'eks', 'rds', 'dynamodb', 'terraform', 'cloudformation'
    ];
    
    const messageLower = message.toLowerCase();
    return infrastructureKeywords.some(keyword => messageLower.includes(keyword));
}

function determineRequiredTabs(request) {
    const requiredTabs = {
        'basic': true,  // Always needed
        'performance': false,
        'security': false,
        'cost': false,
        'compliance': false,
        'advanced': false
    };
    
    if (!request) return requiredTabs;
    
    const requestLower = request.toLowerCase();
    
    // Performance requirements - needed for user-facing applications
    if (requestLower.includes('web app') || requestLower.includes('api') || 
        requestLower.includes('website') || requestLower.includes('application') ||
        requestLower.includes('users') || requestLower.includes('traffic') ||
        requestLower.includes('load') || requestLower.includes('scaling')) {
        requiredTabs.performance = true;
    }
    
    // Security requirements - needed for sensitive data or production
    if (requestLower.includes('production') || requestLower.includes('sensitive') ||
        requestLower.includes('compliance') || requestLower.includes('secure') ||
        requestLower.includes('private') || requestLower.includes('internal') ||
        requestLower.includes('vpc') || requestLower.includes('network')) {
        requiredTabs.security = true;
    }
    
    // Cost requirements - needed for budget-conscious projects
    if (requestLower.includes('budget') || requestLower.includes('cost') ||
        requestLower.includes('cheap') || requestLower.includes('affordable') ||
        requestLower.includes('minimal') || requestLower.includes('optimize')) {
        requiredTabs.cost = true;
    }
    
    // Compliance requirements - needed for regulated industries
    if (requestLower.includes('healthcare') || requestLower.includes('finance') ||
        requestLower.includes('banking') || requestLower.includes('government') ||
        requestLower.includes('soc2') || requestLower.includes('hipaa') ||
        requestLower.includes('pci') || requestLower.includes('gdpr')) {
        requiredTabs.compliance = true;
    }
    
    // Advanced requirements - needed for complex deployments
    if (requestLower.includes('blue-green') || requestLower.includes('canary') ||
        requestLower.includes('rolling') || requestLower.includes('disaster recovery') ||
        requestLower.includes('backup') || requestLower.includes('monitoring') ||
        requestLower.includes('logging') || requestLower.includes('multi-cloud') ||
        requestLower.includes('hybrid')) {
        requiredTabs.advanced = true;
    }
    
    // Pattern-specific adjustments
    if (requestLower.includes('serverless') || requestLower.includes('lambda')) {
        requiredTabs.performance = true;
        requiredTabs.cost = true;
    }
    
    if (requestLower.includes('microservices') || requestLower.includes('kubernetes') ||
        requestLower.includes('eks') || requestLower.includes('aks') || requestLower.includes('gke')) {
        requiredTabs.advanced = true;
        requiredTabs.performance = true;
    }
    
    if (requestLower.includes('simple') || requestLower.includes('basic') ||
        requestLower.includes('development') || requestLower.includes('test')) {
        requiredTabs.advanced = false;
        requiredTabs.compliance = false;
    }
    
    return requiredTabs;
}

function showOnlyRequiredTabs(requiredTabs) {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // Show/hide tab buttons based on requirements
    tabButtons.forEach(button => {
        const tabName = button.getAttribute('onclick').match(/'([^']+)'/)[1];
        if (requiredTabs[tabName]) {
            button.style.display = 'inline-block';
        } else {
            button.style.display = 'none';
        }
    });
    
    // Show/hide tab contents based on requirements
    tabContents.forEach(content => {
        const tabName = content.id;
        if (requiredTabs[tabName]) {
            content.style.display = 'block';
        } else {
            content.style.display = 'none';
        }
    });
    
    // Update tabs array to only include required tabs
    tabs = Object.keys(requiredTabs).filter(tab => requiredTabs[tab]);
}
