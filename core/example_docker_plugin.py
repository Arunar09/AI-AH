#!/usr/bin/env python3
"""
Example Docker Plugin
====================

This is an example implementation of a tool plugin for Docker.
It demonstrates how to create plugins for the base agent system.
"""

from typing import Dict, List, Any
from .plugin_system import ToolPlugin, PluginCapability, PluginResponse


class DockerPlugin(ToolPlugin):
    """
    Example Docker plugin implementation
    
    This plugin provides Docker-specific knowledge and capabilities
    """
    
    def _init_capabilities(self) -> List[PluginCapability]:
        """Initialize Docker-specific capabilities"""
        return [
            PluginCapability(
                name="Docker Basics",
                description="Explain Docker concepts and basics",
                keywords=["what", "explain", "docker", "container"],
                confidence_threshold=0.7,
                can_execute_tools=False
            ),
            PluginCapability(
                name="Docker Commands",
                description="Help with Docker commands and usage",
                keywords=["docker", "run", "build", "command", "how"],
                confidence_threshold=0.8,
                can_execute_tools=True
            ),
            PluginCapability(
                name="Docker Troubleshooting",
                description="Help troubleshoot Docker issues",
                keywords=["docker", "error", "problem", "not working", "fix"],
                confidence_threshold=0.75,
                can_execute_tools=False
            )
        ]
    
    def can_handle(self, query_analysis: Dict[str, Any]) -> float:
        """Determine if this plugin can handle the Docker-related query"""
        keywords = query_analysis.get('keywords', [])
        context = query_analysis.get('context', {})
        intent = query_analysis.get('intent', 'general')
        
        # Check for Docker-specific keywords (more specific to avoid false positives)
        docker_keywords = ['docker', 'container', 'dockerfile', 'image', 'containerize', 'containerization', 'docker networking', 'docker troubleshooting', 'docker volume', 'docker build']
        docker_score = sum(1 for keyword in keywords if keyword.lower() in docker_keywords)
        
        # Check tools mentioned in context
        tools_mentioned = context.get('tools_mentioned', [])
        tool_score = 1 if 'docker' in tools_mentioned else 0
        
        # Calculate base confidence
        if docker_score > 0 or tool_score > 0:
            confidence = min(0.4 + (docker_score * 0.3) + (tool_score * 0.4), 1.0)
            
            # Boost confidence for relevant intents
            if intent in ['information_request', 'command_request', 'troubleshooting']:
                confidence += 0.2
                
            # Additional boost for command requests (like "How do I run")
            if intent == 'command_request':
                confidence += 0.1
                
            return min(confidence, 1.0)
        
        return 0.0
    
    def get_knowledge(self, keywords: List[str], context: Dict[str, Any]) -> PluginResponse:
        """Get Docker-specific knowledge based on keywords"""
        
        keywords_lower = [k.lower() for k in keywords]
        
        # Docker basics
        if any(word in keywords_lower for word in ['what', 'explain', 'docker', 'container', 'containerization', 'image', 'volume', 'networking']):
            content = self._get_docker_basics()
            return PluginResponse(
                success=True,
                content=content,
                confidence=0.9,
                source=self.name,
                additional_data={'topic': 'docker_basics'}
            )
        
        # Docker commands
        if any(word in keywords_lower for word in ['run', 'build', 'command', 'how', 'start', 'create', 'dockerfile', 'installation', 'install', 'guide', 'container', 'execute']):
            content = self._get_docker_commands(keywords_lower)
            return PluginResponse(
                success=True,
                content=content,
                confidence=0.9,
                source=self.name,
                additional_data={'topic': 'docker_commands'}
            )
        
        # Docker troubleshooting
        if any(word in keywords_lower for word in ['error', 'problem', 'not working', 'fix', 'troubleshoot', 'troubleshooting', 'debug', 'issue', 'broken']):
            content = self._get_docker_troubleshooting()
            return PluginResponse(
                success=True,
                content=content,
                confidence=0.8,
                source=self.name,
                additional_data={'topic': 'docker_troubleshooting'}
            )
        
        # Installation
        if any(word in keywords_lower for word in ['install', 'setup', 'configure']):
            content = self._get_docker_installation()
            return PluginResponse(
                success=True,
                content=content,
                confidence=0.85,
                source=self.name,
                additional_data={'topic': 'docker_installation'}
            )
        
        # Generic Docker help
        content = "I can help you with Docker! Ask me about:\n\n• Docker basics and concepts\n• Docker commands and usage\n• Docker installation\n• Troubleshooting Docker issues\n\nWhat specific aspect of Docker interests you?"
        
        return PluginResponse(
            success=True,
            content=content,
            confidence=0.7,
            source=self.name,
            additional_data={'topic': 'docker_general'}
        )
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> PluginResponse:
        """Execute Docker commands (example implementation)"""
        
        # This is a simplified example - real implementation would use subprocess
        # and proper security measures
        
        if tool_name == "docker_info":
            return PluginResponse(
                success=True,
                content="Docker system information would be displayed here (simulated)",
                confidence=0.9,
                source=self.name,
                additional_data={'command': 'docker info'}
            )
        
        elif tool_name == "docker_version":
            return PluginResponse(
                success=True,
                content="Docker version information would be displayed here (simulated)",
                confidence=0.9,
                source=self.name,
                additional_data={'command': 'docker version'}
            )
        
        else:
            return PluginResponse(
                success=False,
                content=f"Unknown Docker tool: {tool_name}",
                confidence=0.0,
                source=self.name,
                additional_data={'error': 'unknown_tool'}
            )
    
    def _get_docker_basics(self) -> str:
        """Get Docker basics explanation"""
        return """Docker is a containerization platform that allows you to package applications and their dependencies into lightweight, portable containers.

**Key Concepts:**

• **Container**: A lightweight, portable package that includes everything needed to run an application
• **Image**: A template used to create containers
• **Dockerfile**: A text file with instructions to build a Docker image
• **Registry**: A storage location for Docker images (like Docker Hub)

**Benefits:**
• Consistent environments across development, testing, and production
• Improved resource utilization
• Easy scaling and deployment
• Simplified dependency management"""
    
    def _get_docker_commands(self, keywords: List[str]) -> str:
        """Get Docker commands based on keywords"""
        
        # Check for specific command keywords
        if 'run' in keywords or 'container' in keywords:
            return """**How to Run a Docker Container:**

```bash
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

**Common examples:**
```bash
# Run a simple container
docker run hello-world

# Run container interactively
docker run -it ubuntu bash

# Run container with port mapping
docker run -p 8080:80 nginx

# Run container in background
docker run -d nginx

# Run with custom name
docker run --name myapp nginx
```

**Essential options:**
• `-it`: Interactive mode with terminal
• `-d`: Run in background (detached)
• `-p`: Port mapping (host:container)
• `--name`: Give container a name
• `-v`: Volume mounting
• `-e`: Set environment variables

**Step-by-step process:**
1. Pull the image: `docker pull <image>`
2. Run the container: `docker run <options> <image>`
3. Check status: `docker ps`
4. Stop when done: `docker stop <container_id>`"""
        
        elif 'build' in keywords:
            return """**Docker Build Command:**

```bash
docker build [OPTIONS] PATH
```

**Examples:**
```bash
# Build from current directory
docker build .

# Build with custom tag
docker build -t myapp:latest .

# Build with Dockerfile in different location
docker build -f /path/to/Dockerfile .
```

**Common Dockerfile instructions:**
• `FROM`: Base image
• `COPY`: Copy files into image
• `RUN`: Execute commands
• `EXPOSE`: Expose ports
• `CMD`: Default command to run"""
        
        else:
            return """**Essential Docker Commands:**

**Image Management:**
```bash
docker images          # List images
docker pull <image>     # Download image
docker rmi <image>      # Remove image
```

**Container Management:**
```bash
docker ps              # List running containers
docker ps -a           # List all containers
docker start <id>      # Start container
docker stop <id>       # Stop container
docker rm <id>         # Remove container
```

**Build and Run:**
```bash
docker build -t <name> .     # Build image
docker run <options> <image> # Run container
```"""
    
    def _get_docker_installation(self) -> str:
        """Get Docker installation instructions"""
        return """**Docker Installation:**

**Windows:**
1. Download Docker Desktop from docker.com
2. Run the installer
3. Enable WSL 2 integration if prompted
4. Restart your computer
5. Verify: `docker --version`

**macOS:**
1. Download Docker Desktop from docker.com
2. Drag to Applications folder
3. Launch Docker Desktop
4. Verify: `docker --version`

**Linux (Ubuntu/Debian):**
```bash
# Update package index
sudo apt update

# Install prerequisites
sudo apt install apt-transport-https ca-certificates curl software-properties-common

# Add Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add Docker repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Install Docker
sudo apt update
sudo apt install docker-ce

# Add user to docker group
sudo usermod -aG docker $USER
```

**Verify Installation:**
```bash
docker --version
docker run hello-world
```"""
    
    def _get_docker_troubleshooting(self) -> str:
        """Get Docker troubleshooting information"""
        return """**Common Docker Issues and Solutions:**

**1. Permission Denied Error**
```
Error: Got permission denied while trying to connect to Docker daemon
```
**Solution:** Add user to docker group:
```bash
sudo usermod -aG docker $USER
# Then logout and login again
```

**2. Port Already in Use**
```
Error: Port 8080 is already allocated
```
**Solution:** Use different port or stop conflicting service:
```bash
docker run -p 8081:80 myapp  # Use different port
# Or find and stop the conflicting container
docker ps | grep 8080
```

**3. Image Not Found**
```
Error: Unable to find image 'myapp:latest' locally
```
**Solution:** Build the image first or check image name:
```bash
docker build -t myapp:latest .
docker images  # List available images
```

**4. Container Exits Immediately**
**Solution:** 
• Check if the main process exits
• Use `docker logs <container-id>` to see output
• Run interactively: `docker run -it <image> bash`

**5. Docker Daemon Not Running**
**Solution:**
• Windows/Mac: Start Docker Desktop
• Linux: `sudo systemctl start docker`"""


# Example usage
if __name__ == "__main__":
    print("🐳 Docker Plugin - Test Mode\n")
    
    # Create plugin
    docker_config = {
        'name': 'Docker Assistant',
        'version': '1.0.0',
        'description': 'Docker containerization platform assistant',
        'keywords': ['docker', 'container', 'containerize', 'dockerfile', 'image'],
        'confidence_threshold': 0.6
    }
    
    plugin = DockerPlugin(docker_config)
    
    # Test query analysis
    test_queries = [
        {
            'keywords': ['docker', 'what', 'is'],
            'context': {'tools_mentioned': ['docker']},
            'intent': 'information_request'
        },
        {
            'keywords': ['docker', 'run', 'command'],
            'context': {},
            'intent': 'command_request'
        },
        {
            'keywords': ['install', 'docker'],
            'context': {},
            'intent': 'command_request'
        }
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"Test {i}: {query['keywords']}")
        
        # Test can_handle
        confidence = plugin.can_handle(query)
        print(f"  Can handle: {confidence:.2f}")
        
        # Test get_knowledge
        if confidence > 0.5:
            response = plugin.get_knowledge(query['keywords'], query['context'])
            print(f"  Response: {response.content[:100]}...")
            print(f"  Confidence: {response.confidence:.2f}")
        
        print("-" * 50)
