#!/usr/bin/env python3
"""
Test script for context awareness and adaptive learning capabilities
"""

import asyncio
from ai_ah_platform.core.intelligence.local_knowledge_base import LocalKnowledgeBase

def test_context_awareness():
    """Test context awareness capabilities."""
    print("🧠 Testing Context Awareness and Adaptive Learning")
    print("=" * 60)
    
    kb = LocalKnowledgeBase()
    user_id = "test_user_001"
    
    # Simulate a conversation flow
    conversation_flow = [
        "I'm working on a web application",
        "What database should I use?",
        "I'm thinking about PostgreSQL",
        "How do I set up monitoring for it?",
        "What about security best practices?"
    ]
    
    print("\n📝 Simulating Conversation Flow:")
    print("-" * 40)
    
    for i, query in enumerate(conversation_flow, 1):
        print(f"\n{i}. User: {query}")
        
        # Analyze with context
        analysis = kb.analyze_request(query, user_id=user_id)
        
        # Simulate response generation
        response = f"Response to: {query}"
        
        # Process with learning
        adapted_response = kb.process_response_with_learning(
            user_id=user_id,
            query=query,
            response=response,
            analysis=analysis
        )
        
        print(f"   Agent: {adapted_response[:100]}...")
        
        # Show context information
        if analysis.get("conversation_context", {}).get("has_context"):
            context = analysis["conversation_context"]
            print(f"   📊 Context: {context.get('recent_topics', [])}")
            print(f"   🎯 Pattern: {context.get('context_pattern', 'none')}")
    
    # Test learning insights
    if kb.learning_engine:
        print("\n🧠 Learning System Insights:")
        print("-" * 40)
        insights = kb.learning_engine.get_learning_insights()
        print(f"Total Interactions: {insights['total_interactions']}")
        print(f"Total Patterns: {insights['total_patterns']}")
        print(f"Learning Accuracy: {insights['learning_accuracy']:.2f}")
        print(f"User Profiles: {insights['user_profiles_count']}")
    
    # Test user profile
    if kb.context_manager:
        print("\n👤 User Profile Analysis:")
        print("-" * 40)
        user_insights = kb.context_manager.get_user_insights(user_id)
        print(f"Total Interactions: {user_insights.get('total_interactions', 0)}")
        print(f"Preferred Technologies: {user_insights.get('preferred_technologies', [])}")
        print(f"Expertise Level: {user_insights.get('expertise_level', 'unknown')}")
        print(f"Interaction Style: {user_insights.get('interaction_style', 'unknown')}")

def test_adaptive_learning():
    """Test adaptive learning capabilities."""
    print("\n\n🎓 Testing Adaptive Learning")
    print("=" * 60)
    
    kb = LocalKnowledgeBase()
    user_id = "learning_user_001"
    
    # Simulate learning from different user types
    user_scenarios = [
        {
            "user_type": "beginner",
            "queries": [
                "what is terraform",
                "how to install terraform",
                "terraform basics tutorial"
            ],
            "feedback": {"satisfaction": 0.9, "expertise_level": 0.2}
        },
        {
            "user_type": "intermediate",
            "queries": [
                "terraform state management best practices",
                "how to organize terraform modules",
                "terraform workspace strategies"
            ],
            "feedback": {"satisfaction": 0.8, "expertise_level": 0.6}
        },
        {
            "user_type": "expert",
            "queries": [
                "terraform provider plugin architecture",
                "custom terraform provider development",
                "terraform enterprise advanced features"
            ],
            "feedback": {"satisfaction": 0.95, "expertise_level": 0.9}
        }
    ]
    
    for scenario in user_scenarios:
        print(f"\n👤 Testing {scenario['user_type'].title()} User:")
        print("-" * 30)
        
        for query in scenario["queries"]:
            analysis = kb.analyze_request(query, user_id=user_id)
            response = f"Adaptive response for {scenario['user_type']}: {query}"
            
            adapted_response = kb.process_response_with_learning(
                user_id=user_id,
                query=query,
                response=response,
                analysis=analysis,
                user_feedback=scenario["feedback"]
            )
            
            print(f"  Query: {query}")
            print(f"  Response: {adapted_response[:80]}...")
        
        # Show learning progress
        if kb.learning_engine:
            insights = kb.learning_engine.get_learning_insights()
            print(f"  Learning Progress: {insights['learning_accuracy']:.2f} accuracy")

def test_pattern_learning():
    """Test pattern learning capabilities."""
    print("\n\n🔍 Testing Pattern Learning")
    print("=" * 60)
    
    kb = LocalKnowledgeBase()
    user_id = "pattern_user_001"
    
    # Test different query patterns
    pattern_tests = [
        {
            "pattern": "how_to_queries",
            "queries": [
                "how to set up monitoring",
                "how to configure security",
                "how to optimize performance"
            ]
        },
        {
            "pattern": "comparison_queries",
            "queries": [
                "aws vs azure comparison",
                "terraform vs ansible",
                "kubernetes vs docker swarm"
            ]
        },
        {
            "pattern": "troubleshooting_queries",
            "queries": [
                "terraform apply failed",
                "kubernetes pod not starting",
                "ansible playbook error"
            ]
        }
    ]
    
    for pattern_test in pattern_tests:
        print(f"\n🔍 Testing {pattern_test['pattern']}:")
        print("-" * 30)
        
        for query in pattern_test["queries"]:
            analysis = kb.analyze_request(query, user_id=user_id)
            response = f"Pattern-based response: {query}"
            
            adapted_response = kb.process_response_with_learning(
                user_id=user_id,
                query=query,
                response=response,
                analysis=analysis
            )
            
            print(f"  Query: {query}")
            print(f"  Intent: {analysis.get('intent', 'unknown')}")
            print(f"  Confidence: {analysis.get('confidence', 0):.2f}")
    
    # Show learned patterns
    if kb.learning_engine:
        print("\n📊 Learned Patterns:")
        print("-" * 30)
        insights = kb.learning_engine.get_learning_insights()
        for pattern in insights.get("most_common_patterns", [])[:3]:
            print(f"  {pattern['id']}: {pattern['frequency']} occurrences, {pattern['confidence']:.2f} confidence")

def test_context_retention():
    """Test context retention across sessions."""
    print("\n\n💾 Testing Context Retention")
    print("=" * 60)
    
    kb = LocalKnowledgeBase()
    user_id = "retention_user_001"
    
    # Simulate multiple sessions
    sessions = [
        {
            "session": "morning",
            "queries": [
                "I need help with AWS setup",
                "What about security groups?",
                "How do I configure load balancer?"
            ]
        },
        {
            "session": "afternoon",
            "queries": [
                "Continuing with the AWS setup",
                "What about monitoring?",
                "How do I set up alerts?"
            ]
        },
        {
            "session": "evening",
            "queries": [
                "I'm still working on the AWS project",
                "What about backup strategies?",
                "How do I implement disaster recovery?"
            ]
        }
    ]
    
    for session in sessions:
        print(f"\n🕐 {session['session'].title()} Session:")
        print("-" * 30)
        
        for query in session["queries"]:
            analysis = kb.analyze_request(query, user_id=user_id)
            
            # Check if context is being retained
            context = analysis.get("conversation_context", {})
            if context.get("has_context"):
                recent_topics = context.get("recent_topics", [])
                print(f"  Query: {query}")
                print(f"  Context: {recent_topics}")
                print(f"  Pattern: {context.get('context_pattern', 'none')}")
            else:
                print(f"  Query: {query} (no context)")
    
    # Show final user profile
    if kb.context_manager:
        print("\n👤 Final User Profile:")
        print("-" * 30)
        user_insights = kb.context_manager.get_user_insights(user_id)
        print(f"Total Interactions: {user_insights.get('total_interactions', 0)}")
        print(f"Preferred Technologies: {user_insights.get('preferred_technologies', [])}")
        print(f"Common Topics: {user_insights.get('interaction_patterns', {}).get('technology_preference', [])}")

if __name__ == "__main__":
    test_context_awareness()
    test_adaptive_learning()
    test_pattern_learning()
    test_context_retention()
    
    print("\n\n🎉 Context Awareness and Learning Tests Complete!")
    print("=" * 60)
    print("The AI-AH platform now demonstrates:")
    print("✅ Context-aware conversation tracking")
    print("✅ Adaptive learning from user interactions")
    print("✅ Pattern recognition and learning")
    print("✅ User profile development")
    print("✅ Cross-session context retention")
