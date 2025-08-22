# Base Agent - Universal AI Agent Foundation

A clean, robust, and extensible AI agent foundation with plugin architecture for building tool-specific assistants.

## 🎯 **Architecture Overview**

The Base Agent follows your specified flow with enhancements for robustness and efficiency:

```
User Query → Query Analysis → Keyword Extraction → Dictionary Lookup → 
Pattern Matching → Memory Context → Plugin Selection → Knowledge Integration → 
Response Generation → Intelligence Curation → Final Response
```

## 🏗️ **Core Components**

### 1. **Universal Dictionary** (`dictionary.py`)
- **Purpose**: Universal language understanding for all queries
- **Features**: Keyword extraction, intent classification, complexity assessment
- **Output**: Structured query analysis with confidence scoring

### 2. **Pattern Matcher** (`pattern_matcher.py`)
- **Purpose**: Conversation pattern matching and knowledge base
- **Features**: Pattern storage, best match selection, usage tracking
- **Output**: Response templates with confidence scores

### 3. **Memory System** (`memory_system.py`)
- **Purpose**: Conversation memory and context management
- **Features**: Session tracking, user preferences, context awareness
- **Output**: Relevant conversation context and history

### 4. **Plugin System** (`plugin_system.py`)
- **Purpose**: Tool-specific knowledge and capability integration
- **Features**: Plugin registration, knowledge integration, tool execution
- **Output**: Tool-specific responses and capabilities

### 5. **Base Agent** (`base_agent.py`)
- **Purpose**: Main orchestrator that coordinates all systems
- **Features**: Complete query processing, response generation, intelligence curation
- **Output**: Structured, curated responses with metadata

## 🚀 **Quick Start**

### Basic Usage

```python
from base_agent import BaseAgent

# Initialize agent
agent = BaseAgent("MyAgent")

# Start conversation session
session_id = agent.start_session("user123")

# Process queries
response = agent.process_query("Hello, what can you help me with?", session_id)

print(f"Response: {response.response}")
print(f"Confidence: {response.confidence}")
print(f"Intent: {response.intent}")
```

### Adding Plugins

```python
from example_docker_plugin import DockerPlugin

# Create plugin
docker_config = {
    'name': 'Docker Assistant',
    'version': '1.0.0',
    'description': 'Docker containerization assistant',
    'keywords': ['docker', 'container', 'dockerfile'],
    'confidence_threshold': 0.6
}

docker_plugin = DockerPlugin(docker_config)

# Register with agent
agent.register_plugin(docker_plugin)

# Now the agent can handle Docker-specific queries
response = agent.process_query("How do I create a Docker container?", session_id)
```

## 🔌 **Creating Custom Plugins**

### Plugin Template

```python
from plugin_system import ToolPlugin, PluginCapability, PluginResponse

class MyToolPlugin(ToolPlugin):
    def _init_capabilities(self):
        return [
            PluginCapability(
                name="Tool Information",
                description="Provide information about the tool",
                keywords=["what", "explain", "mytool"],
                confidence_threshold=0.7,
                can_execute_tools=False
            )
        ]
    
    def can_handle(self, query_analysis):
        keywords = query_analysis.get('keywords', [])
        # Return confidence score (0.0 to 1.0)
        return 0.8 if 'mytool' in keywords else 0.0
    
    def get_knowledge(self, keywords, context):
        content = "Here's information about MyTool..."
        return PluginResponse(
            success=True,
            content=content,
            confidence=0.9,
            source=self.name,
            additional_data={}
        )
```

## 📁 **Project Structure**

```
AI-AH/
├── base_agent.py              # Main agent orchestrator
├── dictionary.py              # Universal language understanding
├── pattern_matcher.py         # Conversation patterns
├── memory_system.py           # Context and memory
├── plugin_system.py           # Plugin architecture
├── example_docker_plugin.py   # Example plugin implementation
├── test_agent.py              # Test suite
├── README.md                  # This file
└── base_agent.db              # SQLite database (created automatically)
```

## 🧪 **Testing**

Run the test suite to validate functionality:

```bash
python test_agent.py
```

### Test Coverage
- ✅ Basic agent functionality
- ✅ Query processing flow  
- ✅ Conversation memory
- ✅ Pattern matching
- ✅ Plugin integration
- ✅ Response generation

## 📊 **Features**

### Core Capabilities
- ✅ **Universal Language Understanding**: Works with any technical domain
- ✅ **Conversation Patterns**: Pre-built patterns for common interactions
- ✅ **Memory & Context**: Tracks conversation history and user preferences
- ✅ **Plugin Architecture**: Easy integration of tool-specific knowledge
- ✅ **Intelligent Curation**: Enhances responses with context and suggestions

### Plugin System
- ✅ **Standardized Interface**: Consistent plugin development experience
- ✅ **Confidence Scoring**: Automatic selection of best plugins for queries
- ✅ **Knowledge Integration**: Seamless combination of multiple knowledge sources
- ✅ **Tool Execution**: Optional capability for plugins to execute actual tools

### Quality Features
- ✅ **Structured Responses**: Consistent response format with metadata
- ✅ **Confidence Tracking**: Transparency in response quality
- ✅ **Performance Monitoring**: Response time tracking and statistics
- ✅ **Error Handling**: Graceful degradation when components fail

## 🛠️ **Configuration**

### Database Configuration
The agent uses SQLite for data persistence. The database file (`base_agent.db`) is created automatically.

### Memory Settings
```python
# Configure memory system
agent.memory.max_history_length = 10  # Keep last 10 interactions
```

### Plugin Thresholds
```python
# Configure plugin confidence thresholds
plugin_config = {
    'confidence_threshold': 0.7  # Only activate if confidence > 70%
}
```

## 📈 **Monitoring**

Get comprehensive agent statistics:

```python
info = agent.get_agent_info()
print(f"Total patterns: {info['statistics']['patterns']['total_patterns']}")
print(f"Memory interactions: {info['statistics']['memory']['total_interactions']}")
print(f"Plugins registered: {info['statistics']['plugins']['total_plugins']}")
```

## 🎯 **Use Cases**

### Tool-Specific Assistants
- **DevOps Tools**: Docker, Kubernetes, Terraform assistants
- **Cloud Platforms**: AWS, Azure, GCP helpers
- **Development Tools**: Git, IDE, framework assistants
- **System Administration**: Linux, Windows, network tools

### Conversation Types
- **Information Requests**: "What is Docker?"
- **Command Help**: "How do I run a container?"
- **Troubleshooting**: "My container won't start"
- **Learning**: "Explain Kubernetes step by step"

## 🔧 **Extension Points**

### Custom Response Generation
Override response generation for domain-specific formatting:

```python
class CustomAgent(BaseAgent):
    def _curate_response(self, response, query_analysis, memory_context):
        # Custom response formatting
        curated, suggestions = super()._curate_response(response, query_analysis, memory_context)
        # Add custom enhancements
        return curated, suggestions
```

### Custom Pattern Matching
Add domain-specific pattern matching logic:

```python
# Add custom patterns
agent.pattern_matcher.add_pattern(
    category="CUSTOM_CATEGORY",
    keywords="custom keywords here",
    response_template="Custom response template",
    confidence=90.0
)
```

## 🚀 **Next Steps**

1. **Run Tests**: Validate the system works correctly
2. **Create Plugins**: Build plugins for your specific tools
3. **Customize Patterns**: Add domain-specific conversation patterns
4. **Integration**: Integrate with your existing systems
5. **Monitoring**: Set up monitoring and logging for production use

## 🤝 **Contributing**

When extending the system:

1. **Follow the Plugin Interface**: Use the standardized plugin architecture
2. **Add Tests**: Include test cases for new functionality
3. **Document Changes**: Update this README with new features
4. **Maintain Simplicity**: Keep the core system clean and understandable

## 📝 **License**

This project is designed to be a foundation for building AI agents. Use it as needed for your projects.

---

**Built with clean architecture, robust error handling, and extensibility in mind.** 🎯