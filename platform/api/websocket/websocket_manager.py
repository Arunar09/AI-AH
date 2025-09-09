"""
WebSocket manager for the Multi-Agent Infrastructure Intelligence Platform.

This module provides WebSocket functionality for real-time communication
with agents and platform components.
"""

from typing import Dict, List, Any, Optional, Set
from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json
import uuid
from datetime import datetime
import logging

from ..schemas.request_models import WebSocketMessage
from ..schemas.response_models import WebSocketResponse


class ConnectionManager:
    """Manages WebSocket connections."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_connections: Dict[str, Set[str]] = {}
        self.session_connections: Dict[str, Set[str]] = {}
        self.logger = logging.getLogger(__name__)
    
    async def connect(self, websocket: WebSocket, connection_id: str, user_id: str = None, session_id: str = None):
        """Accept a WebSocket connection."""
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = set()
            self.user_connections[user_id].add(connection_id)
        
        if session_id:
            if session_id not in self.session_connections:
                self.session_connections[session_id] = set()
            self.session_connections[session_id].add(connection_id)
        
        self.logger.info(f"WebSocket connection {connection_id} established")
    
    def disconnect(self, connection_id: str):
        """Remove a WebSocket connection."""
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
        
        # Remove from user connections
        for user_id, connections in self.user_connections.items():
            connections.discard(connection_id)
            if not connections:
                del self.user_connections[user_id]
        
        # Remove from session connections
        for session_id, connections in self.session_connections.items():
            connections.discard(connection_id)
            if not connections:
                del self.session_connections[session_id]
        
        self.logger.info(f"WebSocket connection {connection_id} disconnected")
    
    async def send_personal_message(self, message: str, connection_id: str):
        """Send a message to a specific connection."""
        if connection_id in self.active_connections:
            websocket = self.active_connections[connection_id]
            try:
                await websocket.send_text(message)
            except Exception as e:
                self.logger.error(f"Error sending message to {connection_id}: {str(e)}")
                self.disconnect(connection_id)
    
    async def send_json_message(self, data: Dict[str, Any], connection_id: str):
        """Send a JSON message to a specific connection."""
        message = json.dumps(data, default=str)
        await self.send_personal_message(message, connection_id)
    
    async def broadcast_to_user(self, message: str, user_id: str):
        """Broadcast a message to all connections of a user."""
        if user_id in self.user_connections:
            for connection_id in self.user_connections[user_id]:
                await self.send_personal_message(message, connection_id)
    
    async def broadcast_to_session(self, message: str, session_id: str):
        """Broadcast a message to all connections in a session."""
        if session_id in self.session_connections:
            for connection_id in self.session_connections[session_id]:
                await self.send_personal_message(message, connection_id)
    
    async def broadcast_to_all(self, message: str):
        """Broadcast a message to all active connections."""
        for connection_id in list(self.active_connections.keys()):
            await self.send_personal_message(message, connection_id)
    
    def get_connection_count(self) -> int:
        """Get the number of active connections."""
        return len(self.active_connections)
    
    def get_user_connection_count(self, user_id: str) -> int:
        """Get the number of connections for a user."""
        return len(self.user_connections.get(user_id, set()))
    
    def get_session_connection_count(self, session_id: str) -> int:
        """Get the number of connections in a session."""
        return len(self.session_connections.get(session_id, set()))


class WebSocketManager:
    """Manages WebSocket operations and message handling."""
    
    def __init__(self):
        self.connection_manager = ConnectionManager()
        self.message_handlers: Dict[str, callable] = {}
        self.logger = logging.getLogger(__name__)
        
        # Register default message handlers
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Register default message handlers."""
        self.message_handlers["ping"] = self._handle_ping
        self.message_handlers["pong"] = self._handle_pong
        self.message_handlers["echo"] = self._handle_echo
        self.message_handlers["status"] = self._handle_status
        self.message_handlers["subscribe"] = self._handle_subscribe
        self.message_handlers["unsubscribe"] = self._handle_unsubscribe
    
    async def handle_connection(self, websocket: WebSocket, user_id: str = None, session_id: str = None):
        """Handle a WebSocket connection."""
        connection_id = str(uuid.uuid4())
        
        try:
            await self.connection_manager.connect(websocket, connection_id, user_id, session_id)
            
            # Send welcome message
            welcome_message = WebSocketResponse(
                message_type="welcome",
                data={
                    "connection_id": connection_id,
                    "user_id": user_id,
                    "session_id": session_id,
                    "timestamp": datetime.now().isoformat()
                }
            )
            await self.connection_manager.send_json_message(welcome_message.dict(), connection_id)
            
            # Handle messages
            while True:
                try:
                    data = await websocket.receive_text()
                    await self._handle_message(data, connection_id, user_id, session_id)
                except WebSocketDisconnect:
                    break
                except Exception as e:
                    self.logger.error(f"Error handling message from {connection_id}: {str(e)}")
                    error_message = WebSocketResponse(
                        message_type="error",
                        data={
                            "error": str(e),
                            "timestamp": datetime.now().isoformat()
                        }
                    )
                    await self.connection_manager.send_json_message(error_message.dict(), connection_id)
        
        except WebSocketDisconnect:
            self.logger.info(f"WebSocket {connection_id} disconnected")
        except Exception as e:
            self.logger.error(f"Error in WebSocket connection {connection_id}: {str(e)}")
        finally:
            self.connection_manager.disconnect(connection_id)
    
    async def _handle_message(self, data: str, connection_id: str, user_id: str = None, session_id: str = None):
        """Handle an incoming WebSocket message."""
        try:
            message_data = json.loads(data)
            message = WebSocketMessage(**message_data)
            
            # Handle the message
            if message.message_type in self.message_handlers:
                handler = self.message_handlers[message.message_type]
                response = await handler(message, connection_id, user_id, session_id)
                
                if response:
                    await self.connection_manager.send_json_message(response.dict(), connection_id)
            else:
                # Unknown message type
                error_response = WebSocketResponse(
                    message_type="error",
                    data={
                        "error": f"Unknown message type: {message.message_type}",
                        "timestamp": datetime.now().isoformat()
                    }
                )
                await self.connection_manager.send_json_message(error_response.dict(), connection_id)
        
        except json.JSONDecodeError:
            error_response = WebSocketResponse(
                message_type="error",
                data={
                    "error": "Invalid JSON format",
                    "timestamp": datetime.now().isoformat()
                }
            )
            await self.connection_manager.send_json_message(error_response.dict(), connection_id)
        except Exception as e:
            self.logger.error(f"Error processing message from {connection_id}: {str(e)}")
            error_response = WebSocketResponse(
                message_type="error",
                data={
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
            )
            await self.connection_manager.send_json_message(error_response.dict(), connection_id)
    
    async def _handle_ping(self, message: WebSocketMessage, connection_id: str, user_id: str = None, session_id: str = None) -> WebSocketResponse:
        """Handle ping message."""
        return WebSocketResponse(
            message_type="pong",
            data={
                "timestamp": datetime.now().isoformat(),
                "connection_id": connection_id
            }
        )
    
    async def _handle_pong(self, message: WebSocketMessage, connection_id: str, user_id: str = None, session_id: str = None) -> WebSocketResponse:
        """Handle pong message."""
        return WebSocketResponse(
            message_type="pong_received",
            data={
                "timestamp": datetime.now().isoformat(),
                "connection_id": connection_id
            }
        )
    
    async def _handle_echo(self, message: WebSocketMessage, connection_id: str, user_id: str = None, session_id: str = None) -> WebSocketResponse:
        """Handle echo message."""
        return WebSocketResponse(
            message_type="echo_response",
            data={
                "original_message": message.data,
                "timestamp": datetime.now().isoformat(),
                "connection_id": connection_id
            }
        )
    
    async def _handle_status(self, message: WebSocketMessage, connection_id: str, user_id: str = None, session_id: str = None) -> WebSocketResponse:
        """Handle status request."""
        status_data = {
            "connection_id": connection_id,
            "user_id": user_id,
            "session_id": session_id,
            "active_connections": self.connection_manager.get_connection_count(),
            "user_connections": self.connection_manager.get_user_connection_count(user_id) if user_id else 0,
            "session_connections": self.connection_manager.get_session_connection_count(session_id) if session_id else 0,
            "timestamp": datetime.now().isoformat()
        }
        
        return WebSocketResponse(
            message_type="status_response",
            data=status_data
        )
    
    async def _handle_subscribe(self, message: WebSocketMessage, connection_id: str, user_id: str = None, session_id: str = None) -> WebSocketResponse:
        """Handle subscription request."""
        # This would implement actual subscription logic
        # For now, just acknowledge the subscription
        return WebSocketResponse(
            message_type="subscription_confirmed",
            data={
                "subscription": message.data.get("subscription", "unknown"),
                "timestamp": datetime.now().isoformat(),
                "connection_id": connection_id
            }
        )
    
    async def _handle_unsubscribe(self, message: WebSocketMessage, connection_id: str, user_id: str = None, session_id: str = None) -> WebSocketResponse:
        """Handle unsubscription request."""
        # This would implement actual unsubscription logic
        # For now, just acknowledge the unsubscription
        return WebSocketResponse(
            message_type="unsubscription_confirmed",
            data={
                "subscription": message.data.get("subscription", "unknown"),
                "timestamp": datetime.now().isoformat(),
                "connection_id": connection_id
            }
        )
    
    def register_handler(self, message_type: str, handler: callable):
        """Register a custom message handler."""
        self.message_handlers[message_type] = handler
        self.logger.info(f"Registered WebSocket handler for message type: {message_type}")
    
    def unregister_handler(self, message_type: str):
        """Unregister a message handler."""
        if message_type in self.message_handlers:
            del self.message_handlers[message_type]
            self.logger.info(f"Unregistered WebSocket handler for message type: {message_type}")
    
    async def send_agent_update(self, agent_type: str, update_data: Dict[str, Any]):
        """Send agent update to all connected clients."""
        message = WebSocketResponse(
            message_type="agent_update",
            data={
                "agent_type": agent_type,
                "update": update_data,
                "timestamp": datetime.now().isoformat()
            }
        )
        await self.connection_manager.broadcast_to_all(json.dumps(message.dict(), default=str))
    
    async def send_task_update(self, task_id: str, update_data: Dict[str, Any]):
        """Send task update to relevant clients."""
        message = WebSocketResponse(
            message_type="task_update",
            data={
                "task_id": task_id,
                "update": update_data,
                "timestamp": datetime.now().isoformat()
            }
        )
        await self.connection_manager.broadcast_to_all(json.dumps(message.dict(), default=str))
    
    async def send_notification(self, user_id: str, notification_data: Dict[str, Any]):
        """Send notification to a specific user."""
        message = WebSocketResponse(
            message_type="notification",
            data={
                "notification": notification_data,
                "timestamp": datetime.now().isoformat()
            }
        )
        await self.connection_manager.broadcast_to_user(json.dumps(message.dict(), default=str), user_id)
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get WebSocket connection statistics."""
        return {
            "total_connections": self.connection_manager.get_connection_count(),
            "user_connections": len(self.connection_manager.user_connections),
            "session_connections": len(self.connection_manager.session_connections),
            "registered_handlers": list(self.message_handlers.keys())
        }


# Global WebSocket manager instance
websocket_manager = WebSocketManager()
