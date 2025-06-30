#!/usr/bin/env python3
"""
Test script to verify tool integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_tool_import():
    """Test that the tool can be imported and initialized."""
    try:
        from tools.progressive_prefix_finder import ProgressivePrefixFinderTool
        tool = ProgressivePrefixFinderTool()
        print(f"✓ Tool imported successfully: {tool.name}")
        print(f"✓ Tool description: {tool.description}")
        print(f"✓ Tool inputs: {list(tool.inputs.keys())}")
        print(f"✓ Tool output type: {tool.output_type}")
        return True
    except Exception as e:
        print(f"✗ Tool import failed: {e}")
        return False

def test_tool_functionality():
    """Test basic tool functionality."""
    try:
        from tools.progressive_prefix_finder import ProgressivePrefixFinderTool
        tool = ProgressivePrefixFinderTool()
        
        # Test with simple case
        test_strings = ["prefix_test_1", "prefix_test_2", "prefix_demo"]
        result = tool.forward(test_strings)
        
        print(f"✓ Tool execution successful")
        print(f"✓ Result type: {type(result)}")
        print(f"✓ Final prefix: '{result['summary']['final_common_prefix']}'")
        print(f"✓ Steps completed: {result['total_steps']}")
        
        # Verify the expected result matches problem statement
        expected_results = [
            ("prefix_test_", 2),  # First 2 strings
            ("prefix_", 3),       # First 3 strings
        ]
        
        for i, (expected_prefix, expected_count) in enumerate(expected_results):
            actual_prefix = result['results'][i]['common_prefix']
            actual_count = result['results'][i]['strings_count']
            
            if actual_prefix == expected_prefix and actual_count == expected_count:
                print(f"✓ Step {i+1} correct: {actual_count} strings -> '{actual_prefix}'")
            else:
                print(f"✗ Step {i+1} mismatch: expected '{expected_prefix}' but got '{actual_prefix}'")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Tool functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_app_imports():
    """Test that app.py can import the new tool."""
    try:
        from tools.progressive_prefix_finder import ProgressivePrefixFinderTool
        from tools.final_answer import FinalAnswerTool
        
        # Test that both tools can be instantiated
        prefix_tool = ProgressivePrefixFinderTool()
        final_tool = FinalAnswerTool()
        
        print(f"✓ Progressive prefix tool: {prefix_tool.name}")
        print(f"✓ Final answer tool: {final_tool.name}")
        
        return True
    except Exception as e:
        print(f"✗ App imports test failed: {e}")
        return False

def main():
    """Run all integration tests."""
    print("Progressive Prefix Finder Tool - Integration Tests")
    print("=" * 60)
    
    tests = [
        ("Tool Import", test_tool_import),
        ("Tool Functionality", test_tool_functionality),
        ("App Imports", test_app_imports),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 40)
        if test_func():
            passed += 1
            print(f"✓ {test_name} PASSED")
        else:
            print(f"✗ {test_name} FAILED")
    
    print("\n" + "=" * 60)
    print(f"Integration Tests: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All integration tests passed!")
        return 0
    else:
        print("❌ Some integration tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())