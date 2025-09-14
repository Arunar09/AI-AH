#!/usr/bin/env python3
"""
Simple CodeLlama Test
Tests basic local model functionality
"""

import os
import sys

# Add the project root to the path
sys.path.append(os.path.dirname(__file__))

def test_basic_imports():
    """Test basic imports"""
    print("🔍 Testing Basic Imports...")
    
    try:
        # Test llama-cpp-python import
        from llama_cpp import Llama
        print("✅ llama-cpp-python imported successfully")
        
        # Test if model file exists
        model_path = r"C:\Users\arunk\.lmstudio\models\TheBloke\codellama\codellama-7b-instruct.Q5_K_M.gguf"
        if os.path.exists(model_path):
            print(f"✅ Model file found at: {model_path}")
            return True
        else:
            print(f"❌ Model file not found at: {model_path}")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Other error: {e}")
        return False

def test_model_loading():
    """Test loading the model"""
    print("\n🤖 Testing Model Loading...")
    
    try:
        from llama_cpp import Llama
        
        model_path = r"C:\Users\arunk\.lmstudio\models\TheBloke\codellama\codellama-7b-instruct.Q5_K_M.gguf"
        
        if not os.path.exists(model_path):
            print("❌ Model file not found")
            return False
        
        print("🔄 Loading model... (this may take a moment)")
        model = Llama(
            model_path=model_path,
            n_ctx=2048,  # Smaller context for testing
            n_threads=2,  # Fewer threads for testing
            verbose=False
        )
        
        print("✅ Model loaded successfully!")
        
        # Test a simple generation
        print("🔄 Testing generation...")
        response = model(
            "<s>[INST] Write a simple Python function to add two numbers. [/INST]",
            max_tokens=100,
            temperature=0.3,
            stop=["</s>", "\n\n\n"],
            echo=False
        )
        
        content = response['choices'][0]['text'].strip()
        print(f"✅ Generation successful!")
        print(f"📝 Response: {content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def main():
    """Run tests"""
    print("🚀 Starting Simple CodeLlama Tests\n")
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Model Loading", test_model_loading)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! CodeLlama is working!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
