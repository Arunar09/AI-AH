"""
WebSocket routes for the Multi-Agent Infrastructure Intelligence Platform API.

This module defines WebSocket endpoints for real-time communication.
"""

from typing import Optional
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends
from fastapi.responses import HTMLResponse
import json

from .websocket_manager import websocket_manager


# Create router
router = APIRouter(prefix="/ws", tags=["websocket"])


@router.websocket("/connect")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: Optional[str] = Query(None),
    session_id: Optional[str] = Query(None)
):
    """WebSocket endpoint for real-time communication."""
    await websocket_manager.handle_connection(websocket, user_id, session_id)


@router.websocket("/agent/{agent_type}")
async def agent_websocket_endpoint(
    websocket: WebSocket,
    agent_type: str,
    user_id: Optional[str] = Query(None),
    session_id: Optional[str] = Query(None)
):
    """WebSocket endpoint for agent-specific communication."""
    # Register agent-specific message handlers
    def register_agent_handlers():
        websocket_manager.register_handler(f"{agent_type}_request", handle_agent_request)
        websocket_manager.register_handler(f"{agent_type}_status", handle_agent_status)
        websocket_manager.register_handler(f"{agent_type}_task", handle_agent_task)
    
    register_agent_handlers()
    
    try:
        await websocket_manager.handle_connection(websocket, user_id, session_id)
    finally:
        # Clean up agent-specific handlers
        websocket_manager.unregister_handler(f"{agent_type}_request")
        websocket_manager.unregister_handler(f"{agent_type}_status")
        websocket_manager.unregister_handler(f"{agent_type}_task")


@router.websocket("/session/{session_id}")
async def session_websocket_endpoint(
    websocket: WebSocket,
    session_id: str,
    user_id: Optional[str] = Query(None)
):
    """WebSocket endpoint for session-specific communication."""
    await websocket_manager.handle_connection(websocket, user_id, session_id)


@router.get("/test")
async def websocket_test_page():
    """Simple HTML page for testing WebSocket connections."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebSocket Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .container { max-width: 800px; margin: 0 auto; }
            .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
            .connected { background-color: #d4edda; color: #155724; }
            .disconnected { background-color: #f8d7da; color: #721c24; }
            .message { background-color: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 3px; }
            input, button { padding: 8px; margin: 5px; }
            #messages { height: 300px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>AI-AH Platform WebSocket Test</h1>
            
            <div id="status" class="status disconnected">Disconnected</div>
            
            <div>
                <input type="text" id="user_id" placeholder="User ID (optional)" value="test_user">
                <input type="text" id="session_id" placeholder="Session ID (optional)" value="test_session">
                <button onclick="connect()">Connect</button>
                <button onclick="disconnect()">Disconnect</button>
            </div>
            
            <div>
                <input type="text" id="message_type" placeholder="Message Type" value="echo">
                <input type="text" id="message_data" placeholder="Message Data" value='{"text": "Hello World"}'>
                <button onclick="sendMessage()">Send Message</button>
            </div>
            
            <div>
                <button onclick="sendPing()">Send Ping</button>
                <button onclick="requestStatus()">Request Status</button>
                <button onclick="subscribe()">Subscribe</button>
                <button onclick="unsubscribe()">Unsubscribe</button>
            </div>
            
            <h3>Messages:</h3>
            <div id="messages"></div>
        </div>

        <script>
            let ws = null;
            let connectionId = null;

            function connect() {
                const user_id = document.getElementById('user_id').value;
                const session_id = document.getElementById('session_id').value;
                
                let url = 'ws://localhost:8000/ws/connect';
                const params = new URLSearchParams();
                if (user_id) params.append('user_id', user_id);
                if (session_id) params.append('session_id', session_id);
                if (params.toString()) url += '?' + params.toString();
                
                ws = new WebSocket(url);
                
                ws.onopen = function(event) {
                    updateStatus('Connected', 'connected');
                    addMessage('Connected to WebSocket', 'system');
                };
                
                ws.onmessage = function(event) {
                    try {
                        const data = JSON.parse(event.data);
                        addMessage(JSON.stringify(data, null, 2), 'received');
                        
                        if (data.message_type === 'welcome') {
                            connectionId = data.data.connection_id;
                        }
                    } catch (e) {
                        addMessage(event.data, 'received');
                    }
                };
                
                ws.onclose = function(event) {
                    updateStatus('Disconnected', 'disconnected');
                    addMessage('WebSocket connection closed', 'system');
                };
                
                ws.onerror = function(error) {
                    updateStatus('Error', 'disconnected');
                    addMessage('WebSocket error: ' + error, 'error');
                };
            }

            function disconnect() {
                if (ws) {
                    ws.close();
                    ws = null;
                }
            }

            function sendMessage() {
                if (!ws || ws.readyState !== WebSocket.OPEN) {
                    alert('WebSocket is not connected');
                    return;
                }
                
                const messageType = document.getElementById('message_type').value;
                const messageData = document.getElementById('message_data').value;
                
                try {
                    const data = JSON.parse(messageData);
                    const message = {
                        message_type: messageType,
                        data: data,
                        timestamp: new Date().toISOString()
                    };
                    
                    ws.send(JSON.stringify(message));
                    addMessage('Sent: ' + JSON.stringify(message, null, 2), 'sent');
                } catch (e) {
                    alert('Invalid JSON in message data: ' + e.message);
                }
            }

            function sendPing() {
                if (!ws || ws.readyState !== WebSocket.OPEN) {
                    alert('WebSocket is not connected');
                    return;
                }
                
                const message = {
                    message_type: 'ping',
                    data: {},
                    timestamp: new Date().toISOString()
                };
                
                ws.send(JSON.stringify(message));
                addMessage('Sent ping', 'sent');
            }

            function requestStatus() {
                if (!ws || ws.readyState !== WebSocket.OPEN) {
                    alert('WebSocket is not connected');
                    return;
                }
                
                const message = {
                    message_type: 'status',
                    data: {},
                    timestamp: new Date().toISOString()
                };
                
                ws.send(JSON.stringify(message));
                addMessage('Requested status', 'sent');
            }

            function subscribe() {
                if (!ws || ws.readyState !== WebSocket.OPEN) {
                    alert('WebSocket is not connected');
                    return;
                }
                
                const message = {
                    message_type: 'subscribe',
                    data: {
                        subscription: 'agent_updates'
                    },
                    timestamp: new Date().toISOString()
                };
                
                ws.send(JSON.stringify(message));
                addMessage('Subscribed to agent_updates', 'sent');
            }

            function unsubscribe() {
                if (!ws || ws.readyState !== WebSocket.OPEN) {
                    alert('WebSocket is not connected');
                    return;
                }
                
                const message = {
                    message_type: 'unsubscribe',
                    data: {
                        subscription: 'agent_updates'
                    },
                    timestamp: new Date().toISOString()
                };
                
                ws.send(JSON.stringify(message));
                addMessage('Unsubscribed from agent_updates', 'sent');
            }

            function updateStatus(text, className) {
                const status = document.getElementById('status');
                status.textContent = text;
                status.className = 'status ' + className;
            }

            function addMessage(text, type) {
                const messages = document.getElementById('messages');
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message';
                messageDiv.innerHTML = '<strong>' + type.toUpperCase() + ':</strong> ' + text;
                messages.appendChild(messageDiv);
                messages.scrollTop = messages.scrollHeight;
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


async def handle_agent_request(message, connection_id, user_id=None, session_id=None):
    """Handle agent request message."""
    from ..schemas.response_models import WebSocketResponse
    
    return WebSocketResponse(
        message_type="agent_request_response",
        data={
            "agent_type": message.data.get("agent_type", "unknown"),
            "request": message.data,
            "timestamp": message.timestamp,
            "connection_id": connection_id
        }
    )


async def handle_agent_status(message, connection_id, user_id=None, session_id=None):
    """Handle agent status request."""
    from ..schemas.response_models import WebSocketResponse
    
    return WebSocketResponse(
        message_type="agent_status_response",
        data={
            "agent_type": message.data.get("agent_type", "unknown"),
            "status": "active",  # Mock status
            "timestamp": message.timestamp,
            "connection_id": connection_id
        }
    )


async def handle_agent_task(message, connection_id, user_id=None, session_id=None):
    """Handle agent task message."""
    from ..schemas.response_models import WebSocketResponse
    
    return WebSocketResponse(
        message_type="agent_task_response",
        data={
            "task_id": message.data.get("task_id", "unknown"),
            "status": "processing",  # Mock status
            "timestamp": message.timestamp,
            "connection_id": connection_id
        }
    )
