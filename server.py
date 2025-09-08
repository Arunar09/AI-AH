#!/usr/bin/env python3
"""
AI-AH Terraform Engineer Agent Server
=====================================

Flask backend server that provides API endpoints for the frontend
to interact with the Terraform Engineer Agent.
"""

import os
import json
import time
import threading
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template_string, Response
from core.base_agent import BaseAgent
from core.terraform_plugin import TerraformPlugin

app = Flask(__name__)

# Global session management
agents = {}
session_timestamps = {}
MAX_SESSIONS = 10  # Maximum number of active sessions
SESSION_TIMEOUT = 3600  # 1 hour timeout
CLEANUP_INTERVAL = 300  # Cleanup every 5 minutes

# Shared Terraform workspace
SHARED_TERRAFORM_DIR = "./web_terraform_workspace"

def cleanup_expired_sessions():
    """Clean up expired sessions automatically"""
    current_time = time.time()
    expired_sessions = []
    
    for session_id, timestamp in session_timestamps.items():
        if current_time - timestamp > SESSION_TIMEOUT:
            expired_sessions.append(session_id)
    
    for session_id in expired_sessions:
        if session_id in agents:
            del agents[session_id]
        if session_id in session_timestamps:
            del session_timestamps[session_id]
        print(f"🧹 Cleaned up expired session: {session_id}")
    
    # If we still have too many sessions, remove oldest ones
    if len(agents) > MAX_SESSIONS:
        sorted_sessions = sorted(session_timestamps.items(), key=lambda x: x[1])
        sessions_to_remove = len(agents) - MAX_SESSIONS
        
        for i in range(sessions_to_remove):
            session_id = sorted_sessions[i][0]
            if session_id in agents:
                del agents[session_id]
            if session_id in session_timestamps:
                del session_timestamps[session_id]
            print(f"🧹 Cleaned up old session due to limit: {session_id}")

def create_session_agent(session_id: str):
    """Create a new agent for a session with shared workspace"""
    try:
        # Create session-specific subdirectory within shared workspace
        session_dir = os.path.join(SHARED_TERRAFORM_DIR, f"session_{session_id}")
        os.makedirs(session_dir, exist_ok=True)
        
        # Create agent with session-specific Terraform directory
        agent = BaseAgent(agent_name=f"TerraformEngineer_{session_id}")
        
        # Create Terraform plugin with proper configuration
        terraform_config = {
            'name': 'Terraform Engineer',
            'version': '2.0.0',
            'description': 'Infrastructure engineering capabilities',
            'terraform_dir': session_dir,
            'keywords': ['terraform', 'infrastructure', 'aws', 'deploy', 'design'],
            'confidence_threshold': 0.5
        }
        agent.terraform_plugin = TerraformPlugin(plugin_config=terraform_config)
        
        # Update timestamps
        session_timestamps[session_id] = time.time()
        
        print(f"🚀 Created new agent for session: {session_id}")
        return agent
        
    except Exception as e:
        print(f"❌ Error creating session agent: {e}")
        return None

def get_session_agent(session_id: str):
    """Get or create an agent for a given session"""
    # Cleanup expired sessions first
    cleanup_expired_sessions()
    
    if session_id not in agents:
        agents[session_id] = create_session_agent(session_id)
    
    # Update session timestamp
    session_timestamps[session_id] = time.time()
    
    return agents[session_id]

@app.route('/')
def index():
    """Serve the main page"""
    with open('frontend/index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files with proper MIME types"""
    try:
        file_path = f'frontend/{filename}'
        
        # Determine MIME type based on file extension
        if filename.endswith('.css'):
            mimetype = 'text/css'
        elif filename.endswith('.js'):
            mimetype = 'application/javascript'
        elif filename.endswith('.html'):
            mimetype = 'text/html'
        elif filename.endswith('.png'):
            mimetype = 'image/png'
        elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
            mimetype = 'image/jpeg'
        elif filename.endswith('.svg'):
            mimetype = 'image/svg+xml'
        else:
            mimetype = 'text/plain'
        
        # Read and serve the file with proper MIME type
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return Response(content, mimetype=mimetype)
            
    except FileNotFoundError:
        return "File not found", 404
    except Exception as e:
        return f"Error serving file: {str(e)}", 500

@app.route('/api/initialize', methods=['POST'])
def api_initialize():
    """Initialize a new session"""
    try:
        data = request.get_json()
        session_id = data.get('session_id', f'session_{int(time.time())}')
        
        # Get or create agent for this session
        agent = get_session_agent(session_id)
        
        if agent:
            return jsonify({
                'success': True,
                'session_id': session_id,
                'message': 'Session initialized successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to initialize session'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        # Get or create agent for this session
        agent = get_session_agent(session_id)
        
        if not agent:
            return jsonify({
                'success': False,
                'error': 'Session not initialized'
            }), 400
        
        # Process the query
        response = agent.process_query(message)
        
        # Handle different response types
        if hasattr(response, 'response'):  # Single AgentResponse
            response_data = {
                'success': True,
                'response': response.response,
                'confidence': getattr(response, 'confidence', 0.9),
                'intent': getattr(response, 'intent', 'general'),
                'plugins_used': getattr(response, 'plugins_used', [])
            }
        else:  # List of PluginResponse
            response_data = {
                'success': True,
                'response': response[0].response if response else 'No response generated',
                'confidence': response[0].confidence if response else 0.9,
                'intent': response[0].intent if response else 'general',
                'plugins_used': response[0].plugins_used if response else []
            }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/execute', methods=['POST'])
def api_execute():
    """Execute Terraform commands"""
    try:
        data = request.get_json()
        command = data.get('command', '')
        session_id = data.get('session_id', 'default')
        
        # Get agent for this session
        agent = get_session_agent(session_id)
        
        if not agent or not hasattr(agent, 'terraform_plugin'):
            return jsonify({
                'success': False,
                'error': 'Terraform plugin not available'
            }), 400
        
        # Execute the command
        result = agent.terraform_plugin.execute_command(command)
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def api_status():
    """Get system status"""
    try:
        # Get active sessions info
        active_sessions = len(agents)
        total_sessions_created = len(session_timestamps)
        
        # Get workspace info
        workspace_exists = os.path.exists(SHARED_TERRAFORM_DIR)
        workspace_size = 0
        if workspace_exists:
            workspace_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                               for dirpath, dirnames, filenames in os.walk(SHARED_TERRAFORM_DIR)
                               for filename in filenames)
        
        return jsonify({
            'success': True,
            'status': 'running',
            'active_sessions': active_sessions,
            'total_sessions_created': total_sessions_created,
            'max_sessions': MAX_SESSIONS,
            'session_timeout': SESSION_TIMEOUT,
            'workspace_exists': workspace_exists,
            'workspace_size_bytes': workspace_size,
            'cleanup_interval': CLEANUP_INTERVAL
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/reset', methods=['POST'])
def api_reset():
    """Reset a session's workspace"""
    try:
        data = request.get_json()
        session_id = data.get('session_id', 'default')
        
        # Get agent for this session
        agent = get_session_agent(session_id)
        
        if not agent or not hasattr(agent, 'terraform_plugin'):
            return jsonify({
                'success': False,
                'error': 'Terraform plugin not available'
            }), 400
        
        # Reset the session's workspace
        session_dir = os.path.join(SHARED_TERRAFORM_DIR, f"session_{session_id}")
        if os.path.exists(session_dir):
            import shutil
            shutil.rmtree(session_dir)
            os.makedirs(session_dir, exist_ok=True)
        
        return jsonify({
            'success': True,
            'message': f'Session {session_id} workspace reset successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/cleanup', methods=['POST'])
def api_cleanup():
    """Manual cleanup of expired sessions"""
    try:
        cleanup_expired_sessions()
        
        return jsonify({
            'success': True,
            'message': 'Cleanup completed',
            'active_sessions': len(agents)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting AI-AH Terraform Engineer Agent Server...")
    
    # Ensure shared workspace exists
    os.makedirs(SHARED_TERRAFORM_DIR, exist_ok=True)
    
    # Start cleanup thread
    def cleanup_thread():
        while True:
            time.sleep(CLEANUP_INTERVAL)
            cleanup_expired_sessions()
    
    cleanup_thread = threading.Thread(target=cleanup_thread, daemon=True)
    cleanup_thread.start()
    
    print("✅ Agent system ready!")
    print(f"🌐 Starting web server on http://localhost:5000")
    print(f"📱 Frontend will be available at http://localhost:5000")
    print(f"🔧 API endpoints available at http://localhost:5000/api/*")
    print("🎯 You can now:")
    print("   • Open http://localhost:5000 in your browser")
    print("   • Chat with the AI Infrastructure Engineer")
    print("   • Design and generate infrastructure")
    print("   • Execute Terraform operations")
    print("   • Troubleshoot infrastructure issues")
    print("🛑 Press Ctrl+C to stop the server")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
