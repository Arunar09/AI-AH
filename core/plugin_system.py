#!/usr/bin/env python3
"""
Plugin System Architecture
==========================

This module provides the plugin architecture for tool-specific knowledge and capabilities.
It enables the base agent to work with different tools through standardized plugins.

Flow: Query Analysis → Plugin Selection → Knowledge Retrieval → Tool Integration
"""

import json
from typing import Dict, List, Any, Optional, Protocol
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class PluginCapability:
    """Defines what a plugin can do"""
    name: str
    description: str
    keywords: List[str]
    confidence_threshold: float
    can_execute_tools: bool


@dataclass
class PluginResponse:
    """Response from a plugin"""
    success: bool
    content: str
    confidence: float
    source: str
    additional_data: Dict[str, Any]


class ToolPlugin(ABC):
    """
    Abstract base class for all tool plugins
    
    Each plugin must implement these methods to integrate with the base agent
    """
    
    def __init__(self, plugin_config: Dict[str, Any]):
        self.name = plugin_config.get('name', 'Unknown Plugin')
        self.version = plugin_config.get('version', '1.0.0')
        self.description = plugin_config.get('description', '')
        self.keywords = plugin_config.get('keywords', [])
        self.confidence_threshold = plugin_config.get('confidence_threshold', 0.7)
        self.capabilities = self._init_capabilities()
    
    @abstractmethod
    def _init_capabilities(self) -> List[PluginCapability]:
        """Initialize plugin capabilities"""
        pass
    
    @abstractmethod
    def can_handle(self, query_analysis: Dict[str, Any]) -> float:
        """
        Determine if this plugin can handle the query
        
        Args:
            query_analysis: Analysis from dictionary system
            
        Returns:
            Confidence score (0.0 to 1.0) that this plugin can help
        """
        pass
    
    @abstractmethod
    def get_knowledge(self, keywords: List[str], context: Dict[str, Any]) -> PluginResponse:
        """
        Get relevant knowledge for the keywords
        
        Args:
            keywords: Extracted keywords from query
            context: Additional context information
            
        Returns:
            PluginResponse with relevant knowledge
        """
        pass
    
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> PluginResponse:
        """
        Execute a tool command (optional implementation)
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters for the tool
            
        Returns:
            PluginResponse with execution results
        """
        return PluginResponse(
            success=False,
            content=f"Tool execution not implemented for {self.name}",
            confidence=0.0,
            source=self.name,
            additional_data={}
        )
    
    def get_help_text(self) -> str:
        """Get help text for this plugin"""
        help_lines = [
            f"# {self.name} Plugin",
            f"{self.description}",
            "",
            "**Capabilities:**"
        ]
        
        for cap in self.capabilities:
            help_lines.append(f"• {cap.name}: {cap.description}")
        
        help_lines.extend([
            "",
            f"**Keywords:** {', '.join(self.keywords)}",
            f"**Version:** {self.version}"
        ])
        
        return "\n".join(help_lines)


class ExamplePlugin(ToolPlugin):
    """Example plugin implementation for reference"""
    
    def _init_capabilities(self) -> List[PluginCapability]:
        return [
            PluginCapability(
                name="Basic Information",
                description="Provide basic information about the tool",
                keywords=["what", "explain", "describe"],
                confidence_threshold=0.8,
                can_execute_tools=False
            ),
            PluginCapability(
                name="Command Help",
                description="Help with tool commands",
                keywords=["command", "how", "run", "execute"],
                confidence_threshold=0.7,
                can_execute_tools=True
            )
        ]
    
    def can_handle(self, query_analysis: Dict[str, Any]) -> float:
        """Check if this plugin can handle the query"""
        keywords = query_analysis.get('keywords', [])
        context = query_analysis.get('context', {})
        
        # Check for plugin-specific keywords
        keyword_matches = sum(1 for keyword in keywords if keyword in self.keywords)
        keyword_score = min(keyword_matches / len(self.keywords), 1.0) if self.keywords else 0
        
        # Check for relevant technical domains
        tools_mentioned = context.get('tools_mentioned', [])
        tool_score = 1.0 if any(tool in self.keywords for tool in tools_mentioned) else 0
        
        # Combine scores
        confidence = (keyword_score * 0.6) + (tool_score * 0.4)
        return confidence
    
    def get_knowledge(self, keywords: List[str], context: Dict[str, Any]) -> PluginResponse:
        """Get knowledge for the query"""
        # This is a simple example - real plugins would have knowledge bases
        content = f"This is example knowledge for keywords: {', '.join(keywords)}"
        
        return PluginResponse(
            success=True,
            content=content,
            confidence=0.8,
            source=self.name,
            additional_data={'keywords_processed': keywords}
        )


class PluginManager:
    """
    Manages all registered plugins and coordinates their usage
    
    Responsibilities:
    1. Register and manage plugins
    2. Select appropriate plugins for queries
    3. Coordinate knowledge retrieval from multiple plugins
    4. Provide unified interface for plugin capabilities
    """
    
    def __init__(self):
        self.plugins: Dict[str, ToolPlugin] = {}
        self.plugin_stats = {}
    
    def register_plugin(self, plugin: ToolPlugin) -> bool:
        """Register a new plugin"""
        try:
            self.plugins[plugin.name] = plugin
            self.plugin_stats[plugin.name] = {
                'queries_handled': 0,
                'successful_responses': 0,
                'average_confidence': 0.0
            }
            print(f"✅ Registered plugin: {plugin.name} v{plugin.version}")
            return True
            
        except Exception as e:
            print(f"❌ Error registering plugin {plugin.name}: {e}")
            return False
    
    def unregister_plugin(self, plugin_name: str) -> bool:
        """Unregister a plugin"""
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]
            del self.plugin_stats[plugin_name]
            print(f"✅ Unregistered plugin: {plugin_name}")
            return True
        return False
    
    def select_plugins(self, query_analysis: Dict[str, Any]) -> List[ToolPlugin]:
        """
        Select relevant plugins for a query
        
        Returns plugins sorted by their confidence in handling the query
        """
        plugin_scores = []
        
        for plugin in self.plugins.values():
            confidence = plugin.can_handle(query_analysis)
            if confidence >= plugin.confidence_threshold:
                plugin_scores.append((plugin, confidence))
        
        # Sort by confidence (highest first)
        plugin_scores.sort(key=lambda x: x[1], reverse=True)
        
        return [plugin for plugin, _ in plugin_scores]
    
    def get_combined_knowledge(self, keywords: List[str], 
                             context: Dict[str, Any],
                             max_plugins: int = 3) -> List[PluginResponse]:
        """
        Get knowledge from relevant plugins
        
        Args:
            keywords: Query keywords
            context: Query context
            max_plugins: Maximum number of plugins to query
            
        Returns:
            List of plugin responses
        """
        # Create query analysis for plugin selection
        query_analysis = {
            'keywords': keywords,
            'context': context
        }
        
        # Select relevant plugins
        relevant_plugins = self.select_plugins(query_analysis)[:max_plugins]
        
        responses = []
        for plugin in relevant_plugins:
            try:
                response = plugin.get_knowledge(keywords, context)
                responses.append(response)
                
                # Update stats
                self._update_plugin_stats(plugin.name, response.confidence, response.success)
                
            except Exception as e:
                print(f"❌ Error getting knowledge from {plugin.name}: {e}")
                # Add error response
                responses.append(PluginResponse(
                    success=False,
                    content=f"Error retrieving knowledge from {plugin.name}",
                    confidence=0.0,
                    source=plugin.name,
                    additional_data={'error': str(e)}
                ))
        
        return responses
    
    def execute_tool_command(self, tool_name: str, plugin_name: str,
                           parameters: Dict[str, Any]) -> PluginResponse:
        """Execute a tool command through a specific plugin"""
        if plugin_name not in self.plugins:
            return PluginResponse(
                success=False,
                content=f"Plugin '{plugin_name}' not found",
                confidence=0.0,
                source="PluginManager",
                additional_data={}
            )
        
        plugin = self.plugins[plugin_name]
        try:
            response = plugin.execute_tool(tool_name, parameters)
            self._update_plugin_stats(plugin_name, response.confidence, response.success)
            return response
            
        except Exception as e:
            print(f"❌ Error executing tool {tool_name} in {plugin_name}: {e}")
            return PluginResponse(
                success=False,
                content=f"Error executing {tool_name}: {str(e)}",
                confidence=0.0,
                source=plugin_name,
                additional_data={'error': str(e)}
            )
    
    def get_plugin_info(self, plugin_name: str = None) -> Dict[str, Any]:
        """Get information about plugins"""
        if plugin_name:
            if plugin_name in self.plugins:
                plugin = self.plugins[plugin_name]
                return {
                    'name': plugin.name,
                    'version': plugin.version,
                    'description': plugin.description,
                    'keywords': plugin.keywords,
                    'capabilities': [
                        {
                            'name': cap.name,
                            'description': cap.description,
                            'keywords': cap.keywords
                        } for cap in plugin.capabilities
                    ],
                    'stats': self.plugin_stats.get(plugin_name, {})
                }
            return {}
        else:
            # Return info for all plugins
            return {
                name: self.get_plugin_info(name) 
                for name in self.plugins.keys()
            }
    
    def _update_plugin_stats(self, plugin_name: str, confidence: float, success: bool):
        """Update plugin usage statistics"""
        stats = self.plugin_stats.get(plugin_name, {})
        
        stats['queries_handled'] = stats.get('queries_handled', 0) + 1
        if success:
            stats['successful_responses'] = stats.get('successful_responses', 0) + 1
        
        # Update average confidence
        old_avg = stats.get('average_confidence', 0.0)
        query_count = stats['queries_handled']
        stats['average_confidence'] = ((old_avg * (query_count - 1)) + confidence) / query_count
        
        self.plugin_stats[plugin_name] = stats
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get overall plugin system statistics"""
        total_plugins = len(self.plugins)
        total_queries = sum(stats.get('queries_handled', 0) for stats in self.plugin_stats.values())
        total_successful = sum(stats.get('successful_responses', 0) for stats in self.plugin_stats.values())
        
        return {
            'total_plugins': total_plugins,
            'total_queries_handled': total_queries,
            'total_successful_responses': total_successful,
            'overall_success_rate': (total_successful / max(total_queries, 1)) * 100,
            'plugin_details': self.plugin_stats
        }


# Example usage and testing
if __name__ == "__main__":
    print("🔌 Plugin System - Test Mode\n")
    
    # Create plugin manager
    manager = PluginManager()
    
    # Create and register example plugin
    example_config = {
        'name': 'Example Tool',
        'version': '1.0.0',
        'description': 'Example plugin for testing',
        'keywords': ['example', 'test', 'demo'],
        'confidence_threshold': 0.5
    }
    
    example_plugin = ExamplePlugin(example_config)
    manager.register_plugin(example_plugin)
    
    # Test plugin selection
    query_analysis = {
        'keywords': ['example', 'help'],
        'context': {'tools_mentioned': ['example']}
    }
    
    selected_plugins = manager.select_plugins(query_analysis)
    print(f"Selected plugins: {[p.name for p in selected_plugins]}")
    
    # Test knowledge retrieval
    responses = manager.get_combined_knowledge(['example', 'test'], {})
    for response in responses:
        print(f"Response from {response.source}: {response.content}")
    
    # Show statistics
    stats = manager.get_system_stats()
    print(f"\nPlugin System Statistics: {stats}")
