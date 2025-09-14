#!/usr/bin/env python3
"""
Test the Local Reasoning Engine
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.reasoning.local_reasoning_engine import LocalReasoningEngine

def test_reasoning_engine():
    """Test the local reasoning engine with a simple scenario"""
    print("🧠 Testing Local Reasoning Engine...")
    
    try:
        # Initialize the reasoning engine
        engine = LocalReasoningEngine()
        print("✅ Reasoning engine initialized successfully")
        
        # Test with a simple request
        request = "I need a web application that can handle 1000 users with a budget of $200/month"
        context = {}
        
        print(f"\n📝 Testing with request: {request}")
        
        # Run reasoning
        result = engine.reason_through_problem(request, context)
        
        print(f"\n🎯 Reasoning Result:")
        print(f"Confidence: {result.confidence:.1%}")
        print(f"Reasoning Steps: {len(result.reasoning_steps)}")
        
        print(f"\n📋 Reasoning Steps:")
        for i, step in enumerate(result.reasoning_steps, 1):
            print(f"{i}. {step}")
        
        print(f"\n💡 Decision:")
        print(f"Solution: {result.decision.solution.name}")
        print(f"Reasoning: {result.decision.reasoning}")
        print(f"Confidence: {result.decision.confidence:.1%}")
        
        print(f"\n📖 Explanation:")
        print(result.explanation)
        
        print(f"\n✅ Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_reasoning_engine()
    if success:
        print("\n🎉 Local Reasoning Engine is working!")
    else:
        print("\n💥 Local Reasoning Engine needs fixes!")
        sys.exit(1)
