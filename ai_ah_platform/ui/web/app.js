/**
 * AI-AH Multi-Agent Infrastructure Intelligence Platform - Web UI
 * 
 * This JavaScript application provides the frontend interface for interacting
 * with the AI-AH platform's specialized agents and monitoring capabilities.
 */

class AIAHPlatform {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8000/api/v1';
        this.wsUrl = 'ws://localhost:8000/ws/connect';
        this.ws = null;
        this.currentUser = null;
        this.currentAgent = null;
        this.chatHistory = [];
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeCharts();
        this.checkAuthentication();
        this.connectWebSocket();
        this.loadDashboardData();
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('nav a').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = e.target.getAttribute('href').substring(1);
                this.showSection(section);
            });
        });

        // Authentication
        document.getElementById('authBtn').addEventListener('click', () => {
            this.showAuthModal();
        });

        document.getElementById('closeAuthModal').addEventListener('click', () => {
            this.hideAuthModal();
        });

        document.getElementById('authForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });

        // Agent selection
        document.querySelectorAll('.agent-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const agent = e.currentTarget.getAttribute('data-agent');
                this.selectAgent(agent);
            });
        });

        // Chat functionality
        document.getElementById('sendBtn').addEventListener('click', () => {
            this.sendChatMessage();
        });

        document.getElementById('chatInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendChatMessage();
            }
        });

        // Quick actions
        document.querySelectorAll('.quick-action').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.currentTarget.getAttribute('data-action');
                this.handleQuickAction(action);
            });
        });
    }

    showSection(sectionName) {
        // Hide all sections
        document.querySelectorAll('.section').forEach(section => {
            section.classList.add('hidden');
        });

        // Show selected section
        const section = document.getElementById(sectionName);
        if (section) {
            section.classList.remove('hidden');
        }

        // Update navigation
        document.querySelectorAll('nav a').forEach(link => {
            link.classList.remove('bg-white', 'bg-opacity-20');
        });
        
        const activeLink = document.querySelector(`nav a[href="#${sectionName}"]`);
        if (activeLink) {
            activeLink.classList.add('bg-white', 'bg-opacity-20');
        }
    }

    async checkAuthentication() {
        const token = localStorage.getItem('auth_token');
        if (token) {
            try {
                const response = await this.apiCall('/auth/me', 'GET', null, token);
                this.currentUser = response;
                this.updateAuthUI(true);
            } catch (error) {
                localStorage.removeItem('auth_token');
                this.updateAuthUI(false);
            }
        } else {
            this.updateAuthUI(false);
        }
    }

    updateAuthUI(isAuthenticated) {
        const authBtn = document.getElementById('authBtn');
        if (isAuthenticated) {
            authBtn.innerHTML = '<i class="fas fa-user mr-1"></i>Logout';
            authBtn.onclick = () => this.logout();
        } else {
            authBtn.innerHTML = '<i class="fas fa-sign-in-alt mr-1"></i>Login';
            authBtn.onclick = () => this.showAuthModal();
        }
    }

    showAuthModal() {
        document.getElementById('authModal').classList.remove('hidden');
    }

    hideAuthModal() {
        document.getElementById('authModal').classList.add('hidden');
    }

    async handleLogin() {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await this.apiCall('/auth/login', 'POST', {
                username: username,
                password: password
            });

            localStorage.setItem('auth_token', response.access_token);
            this.currentUser = response.user;
            this.updateAuthUI(true);
            this.hideAuthModal();
            this.showNotification('Login successful!', 'success');
        } catch (error) {
            this.showNotification('Login failed: ' + error.message, 'error');
        }
    }

    logout() {
        localStorage.removeItem('auth_token');
        this.currentUser = null;
        this.updateAuthUI(false);
        this.showNotification('Logged out successfully', 'info');
    }

    async apiCall(endpoint, method = 'GET', data = null, token = null) {
        const url = this.apiBaseUrl + endpoint;
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };

        if (token) {
            options.headers['Authorization'] = `Bearer ${token}`;
        } else if (this.currentUser) {
            const storedToken = localStorage.getItem('auth_token');
            if (storedToken) {
                options.headers['Authorization'] = `Bearer ${storedToken}`;
            }
        }

        if (data) {
            options.body = JSON.stringify(data);
        }

        const response = await fetch(url, options);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error?.message || 'API request failed');
        }

        return await response.json();
    }

    connectWebSocket() {
        try {
            this.ws = new WebSocket(this.wsUrl);
            
            this.ws.onopen = () => {
                console.log('WebSocket connected');
                this.showNotification('Real-time connection established', 'success');
            };

            this.ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                this.handleWebSocketMessage(data);
            };

            this.ws.onclose = () => {
                console.log('WebSocket disconnected');
                this.showNotification('Real-time connection lost', 'warning');
                // Attempt to reconnect after 5 seconds
                setTimeout(() => this.connectWebSocket(), 5000);
            };

            this.ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.showNotification('WebSocket connection error', 'error');
            };
        } catch (error) {
            console.error('Failed to connect WebSocket:', error);
        }
    }

    handleWebSocketMessage(data) {
        // Fix: Handle the actual WebSocket message structure
        if (data.message_type) {
            switch (data.message_type) {
                case 'agent_update':
                    this.handleAgentUpdate(data.data);
                    break;
                case 'task_update':
                    this.handleTaskUpdate(data.data);
                    break;
                case 'notification':
                    this.showNotification(data.data.notification.message, 'info');
                    break;
                case 'welcome':
                    console.log('WebSocket welcome:', data.data);
                    break;
                case 'pong':
                    console.log('WebSocket pong received');
                    break;
                case 'error':
                    console.error('WebSocket error:', data.data.error);
                    this.showNotification('WebSocket error: ' + data.data.error, 'error');
                    break;
                default:
                    console.log('Unknown WebSocket message:', data);
            }
        } else {
            console.log('Unknown WebSocket message format:', data);
        }
    }

    handleAgentUpdate(data) {
        // Update agent status in the UI
        console.log('Agent update:', data);
        this.loadDashboardData();
    }

    handleTaskUpdate(data) {
        // Update task status in the UI
        console.log('Task update:', data);
        this.updateTaskStatus(data.task_id, data.update);
    }

    async loadDashboardData() {
        try {
            // Load platform status
            const status = await this.apiCall('/platform/status');
            // Fix: Access the correct response structure - metrics is at root level
            this.updateDashboardStats(status.metrics);

            // Load agent statuses
            const agents = await this.apiCall('/agents/');
            // Fix: Access the correct response structure
            this.updateAgentStatuses(agents.data.agents);

        } catch (error) {
            console.error('Failed to load dashboard data:', error);
        }
    }

    updateDashboardStats(status) {
        // Fix: Access the correct properties from the API response
        document.getElementById('activeAgents').textContent = status.agent_statuses ? Object.keys(status.agent_statuses).length : 0;
        document.getElementById('runningTasks').textContent = status.active_tasks || 0;
        document.getElementById('alerts').textContent = status.alerts || 0;
        document.getElementById('successRate').textContent = (status.success_rate || 98.5) + '%';
    }

    updateAgentStatuses(agents) {
        // Update agent status indicators
        agents.forEach(agent => {
            const statusElement = document.querySelector(`[data-agent="${agent.type}"] .status`);
            if (statusElement) {
                statusElement.textContent = agent.status === 'running' ? 'Active' : 'Inactive';
                statusElement.className = `px-2 py-1 rounded-full text-xs ${
                    agent.status === 'running' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
                }`;
            }
        });
    }

    selectAgent(agentType) {
        this.currentAgent = agentType;
        
        // Update UI
        document.querySelectorAll('.agent-btn').forEach(btn => {
            btn.classList.remove('border-blue-500', 'bg-blue-50');
        });
        
        const selectedBtn = document.querySelector(`[data-agent="${agentType}"]`);
        if (selectedBtn) {
            selectedBtn.classList.add('border-blue-500', 'bg-blue-50');
        }

        // Load agent interface
        this.loadAgentInterface(agentType);
    }

    async loadAgentInterface(agentType) {
        const interfaceDiv = document.getElementById('agentInterface');
        
        try {
            // Get agent capabilities
            const capabilities = await this.apiCall(`/agents/${agentType}/capabilities`);
            
            interfaceDiv.innerHTML = `
                <div class="mb-4">
                    <h4 class="font-semibold text-lg mb-2">${this.getAgentDisplayName(agentType)}</h4>
                    <p class="text-gray-600 text-sm mb-4">${this.getAgentDescription(agentType)}</p>
                </div>
                
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Requirements</label>
                        <textarea id="agentRequirements" class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500" rows="4" placeholder="Describe your infrastructure requirements..."></textarea>
                    </div>
                    
                    <div class="flex space-x-3">
                        <button onclick="app.analyzeRequirements('${agentType}')" class="flex-1 bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition-colors">
                            <i class="fas fa-search mr-2"></i>Analyze
                        </button>
                        <button onclick="app.generatePlan('${agentType}')" class="flex-1 bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 transition-colors">
                            <i class="fas fa-magic mr-2"></i>Generate Plan
                        </button>
                        <button onclick="app.executePlan('${agentType}')" class="flex-1 bg-purple-500 text-white py-2 rounded-lg hover:bg-purple-600 transition-colors">
                            <i class="fas fa-play mr-2"></i>Execute
                        </button>
                    </div>
                    
                    <div id="agentResults" class="mt-4"></div>
                </div>
            `;
        } catch (error) {
            interfaceDiv.innerHTML = `
                <div class="text-center text-red-500 py-8">
                    <i class="fas fa-exclamation-triangle text-4xl mb-4"></i>
                    <p>Failed to load agent interface: ${error.message}</p>
                </div>
            `;
        }
    }

    getAgentDisplayName(agentType) {
        const names = {
            'terraform': 'Terraform Agent',
            'ansible': 'Ansible Agent',
            'kubernetes': 'Kubernetes Agent',
            'security': 'Security Agent',
            'monitoring': 'Monitoring Agent'
        };
        return names[agentType] || agentType;
    }

    getAgentDescription(agentType) {
        const descriptions = {
            'terraform': 'Infrastructure provisioning and management with Terraform',
            'ansible': 'Configuration management and automation with Ansible',
            'kubernetes': 'Container orchestration and deployment with Kubernetes',
            'security': 'Security hardening and compliance management',
            'monitoring': 'Infrastructure monitoring and observability'
        };
        return descriptions[agentType] || 'Specialized infrastructure agent';
    }

    async analyzeRequirements(agentType) {
        const requirements = document.getElementById('agentRequirements').value;
        if (!requirements.trim()) {
            this.showNotification('Please enter requirements', 'warning');
            return;
        }

        try {
            const analysis = await this.apiCall(`/agents/${agentType}/analyze`, 'POST', requirements);
            this.displayAgentResults(analysis.data);
        } catch (error) {
            this.showNotification('Analysis failed: ' + error.message, 'error');
        }
    }

    async generatePlan(agentType) {
        const requirements = document.getElementById('agentRequirements').value;
        if (!requirements.trim()) {
            this.showNotification('Please enter requirements', 'warning');
            return;
        }

        try {
            // First analyze requirements
            const analysis = await this.apiCall(`/agents/${agentType}/analyze`, 'POST', requirements);
            
            // Then generate plan
            const plan = await this.apiCall(`/agents/${agentType}/generate`, 'POST', analysis.data);
            this.displayAgentResults(plan.data);
        } catch (error) {
            this.showNotification('Plan generation failed: ' + error.message, 'error');
        }
    }

    async executePlan(agentType) {
        const resultsDiv = document.getElementById('agentResults');
        const existingPlan = resultsDiv.querySelector('.plan-data');
        
        if (!existingPlan) {
            this.showNotification('Please generate a plan first', 'warning');
            return;
        }

        try {
            const planData = JSON.parse(existingPlan.textContent);
            const result = await this.apiCall(`/agents/${agentType}/execute`, 'POST', planData);
            this.displayAgentResults(result.data);
        } catch (error) {
            this.showNotification('Execution failed: ' + error.message, 'error');
        }
    }

    displayAgentResults(data) {
        const resultsDiv = document.getElementById('agentResults');
        
        let html = '<div class="bg-gray-50 rounded-lg p-4">';
        html += '<h5 class="font-semibold mb-2">Results:</h5>';
        
        if (data.status) {
            html += `<p class="text-sm mb-2"><strong>Status:</strong> ${data.status}</p>`;
        }
        
        if (data.message) {
            html += `<p class="text-sm mb-2"><strong>Message:</strong> ${data.message}</p>`;
        }
        
        if (data.plan_id || data.config_id || data.deployment_id || data.assessment_id) {
            const id = data.plan_id || data.config_id || data.deployment_id || data.assessment_id;
            html += `<p class="text-sm mb-2"><strong>ID:</strong> ${id}</p>`;
        }
        
        if (data.resources || data.tasks || data.rules) {
            const count = data.resources || data.tasks || data.rules;
            html += `<p class="text-sm mb-2"><strong>Items:</strong> ${count}</p>`;
        }
        
        html += '</div>';
        
        // Store plan data for execution
        if (data.plan_id || data.config_id || data.deployment_id || data.assessment_id) {
            html += `<div class="plan-data hidden">${JSON.stringify(data)}</div>`;
        }
        
        resultsDiv.innerHTML = html;
    }

    sendChatMessage() {
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message to chat
        this.addChatMessage(message, 'user');
        input.value = '';
        
        // Send to API
        this.sendMessageToAgent(message);
    }

    addChatMessage(message, sender) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message mb-4';
        
        const isUser = sender === 'user';
        const bgColor = isUser ? 'bg-blue-500 text-white' : 'bg-gray-100';
        const alignment = isUser ? 'justify-end' : 'justify-start';
        const icon = isUser ? 'fas fa-user' : 'fas fa-robot';
        const iconBg = isUser ? 'bg-blue-500' : 'bg-gray-500';
        
        messageDiv.innerHTML = `
            <div class="flex items-start ${alignment}">
                ${!isUser ? `
                    <div class="flex-shrink-0">
                        <div class="w-8 h-8 ${iconBg} rounded-full flex items-center justify-center">
                            <i class="${icon} text-white text-sm"></i>
                        </div>
                    </div>
                ` : ''}
                <div class="ml-3 max-w-xs lg:max-w-md">
                    <div class="${bgColor} rounded-lg p-3">
                        <p class="text-sm">${message}</p>
                    </div>
                    <p class="text-xs text-gray-500 mt-1">${isUser ? 'You' : 'AI Assistant'} • Just now</p>
                </div>
                ${isUser ? `
                    <div class="flex-shrink-0 ml-3">
                        <div class="w-8 h-8 ${iconBg} rounded-full flex items-center justify-center">
                            <i class="${icon} text-white text-sm"></i>
                        </div>
                    </div>
                ` : ''}
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async sendMessageToAgent(message) {
        try {
            const response = await this.apiCall('/agents/conversation', 'POST', {
                message: message,
                user_id: this.currentUser?.user_id || 'anonymous',
                session_id: this.getSessionId()
            });
            
            // Fix: Access the correct response structure
            const responseText = response.data?.content || response.data?.response || response.response || 'No response received';
            this.addChatMessage(responseText, 'assistant');
        } catch (error) {
            this.addChatMessage('Sorry, I encountered an error: ' + error.message, 'assistant');
        }
    }

    getSessionId() {
        let sessionId = localStorage.getItem('session_id');
        if (!sessionId) {
            sessionId = 'session_' + Date.now();
            localStorage.setItem('session_id', sessionId);
        }
        return sessionId;
    }

    handleQuickAction(action) {
        const actions = {
            'create-infrastructure': 'I need to create new infrastructure. Can you help me set up a web server with a database?',
            'security-scan': 'Please run a security assessment on my infrastructure.',
            'monitor-status': 'Can you check the status of my infrastructure and show me any issues?',
            'optimize-costs': 'Help me optimize the costs of my cloud infrastructure.'
        };
        
        const message = actions[action];
        if (message) {
            document.getElementById('chatInput').value = message;
            this.sendChatMessage();
            this.showSection('conversation');
        }
    }

    initializeCharts() {
        // Initialize metrics chart
        const ctx = document.getElementById('metricsChart');
        if (ctx) {
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
                    datasets: [{
                        label: 'CPU Usage',
                        data: [20, 25, 30, 35, 40, 45],
                        borderColor: 'rgb(59, 130, 246)',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.4
                    }, {
                        label: 'Memory Usage',
                        data: [40, 45, 50, 55, 60, 65],
                        borderColor: 'rgb(16, 185, 129)',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 max-w-sm ${
            type === 'success' ? 'bg-green-500 text-white' :
            type === 'error' ? 'bg-red-500 text-white' :
            type === 'warning' ? 'bg-yellow-500 text-white' :
            'bg-blue-500 text-white'
        }`;
        
        notification.innerHTML = `
            <div class="flex items-center">
                <i class="fas ${
                    type === 'success' ? 'fa-check-circle' :
                    type === 'error' ? 'fa-exclamation-circle' :
                    type === 'warning' ? 'fa-exclamation-triangle' :
                    'fa-info-circle'
                } mr-2"></i>
                <span>${message}</span>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Remove after 5 seconds
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    updateTaskStatus(taskId, update) {
        // Update task status in the UI
        console.log(`Task ${taskId} status updated:`, update);
    }
}

// Initialize the application
const app = new AIAHPlatform();

// Make app globally available for onclick handlers
window.app = app;
