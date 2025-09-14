#!/usr/bin/env python3
"""
Test Optimized CodeLlama Performance
Tests the speed improvements
"""

import os
import sys
import time

# Add the project root to the path
sys.path.append(os.path.dirname(__file__))

def test_optimized_model():
    """Test optimized model performance"""
    print("🚀 Testing Optimized CodeLlama Performance...")
    
    try:
        sys.path.append('intelligent-agents')
        from core.models.simple_local_model import get_simple_model, is_simple_model_available
        
        if not is_simple_model_available():
            print("❌ Model not available")
            return False
        
        model = get_simple_model()
        
        # Test with a simple prompt
        test_prompt = "<s>[INST] Write a simple Python function to add two numbers. [/INST]"
        
        print("🔄 Testing generation speed...")
        start_time = time.time()
        
        response = model.generate_response(test_prompt, max_tokens=100)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"✅ Generation completed in {response_time:.2f} seconds")
        print(f"📝 Response: {response[:200]}...")
        
        if response_time < 10:
            print("🎉 Performance is good! (< 10 seconds)")
            return True
        elif response_time < 20:
            print("⚠️ Performance is acceptable (< 20 seconds)")
            return True
        else:
            print("❌ Performance is too slow (> 20 seconds)")
            return False
            
    except Exception as e:
        print(f"❌ Error testing optimized model: {e}")
        return False

def main():
    """Run performance test"""
    print("🚀 Starting Optimized CodeLlama Performance Test\n")
    
    success = test_optimized_model()
    
    if success:
        print("\n🎉 CodeLlama optimization successful!")
        print("The model should now respond much faster in the web interface.")
    else:
        print("\n⚠️ Performance issues detected.")
        print("Consider using fallback mode or further optimization.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
