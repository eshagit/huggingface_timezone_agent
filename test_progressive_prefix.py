#!/usr/bin/env python3
"""
Test script for the Progressive Prefix Finder Tool
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.progressive_prefix_finder import ProgressivePrefixFinderTool, AdvancedPrefixAnalyzer


def test_basic_functionality():
    """Test basic progressive prefix finding functionality."""
    print("=" * 60)
    print("Testing Basic Functionality")
    print("=" * 60)
    
    tool = ProgressivePrefixFinderTool()
    
    # Test case from the problem statement
    test_strings = ["prefix_test_1", "prefix_test_2", "prefix_demo", "prefix_example"]
    
    print(f"Input strings: {test_strings}")
    print()
    
    # Test with character algorithm
    result = tool.forward(test_strings, algorithm="character")
    
    print("Results:")
    for step_result in result["results"]:
        print(f"Step {step_result['step']}: {step_result['strings_count']} strings -> '{step_result['common_prefix']}'")
    
    print(f"\nSummary:")
    print(f"Algorithm: {result['algorithm_used']}")
    print(f"Final common prefix: '{result['summary']['final_common_prefix']}'")
    print(f"Prefix length: {result['summary']['prefix_length']}")
    print()


def test_edge_cases():
    """Test edge cases."""
    print("=" * 60)
    print("Testing Edge Cases")
    print("=" * 60)
    
    tool = ProgressivePrefixFinderTool()
    
    # Empty list
    result = tool.forward([])
    print(f"Empty list: {result}")
    
    # Single string
    result = tool.forward(["single_string"])
    print(f"Single string: {result}")
    
    # No common prefix
    result = tool.forward(["abc", "xyz", "123"])
    print(f"No common prefix: {result['summary']}")
    
    # Empty string in list
    result = tool.forward(["", "abc", "ab"])
    print(f"Empty string in list: {result['summary']}")
    print()


def test_algorithms_comparison():
    """Test different algorithms and compare performance."""
    print("=" * 60)
    print("Testing Algorithm Comparison")
    print("=" * 60)
    
    test_strings = ["prefix_test_1", "prefix_test_2", "prefix_demo", "prefix_example"]
    
    comparison = AdvancedPrefixAnalyzer.compare_algorithms(test_strings, include_visualization=True)
    
    print("Algorithm Comparison Results:")
    for algorithm, result in comparison["comparison_results"].items():
        if "error" not in result:
            final_prefix = result["summary"]["final_common_prefix"]
            print(f"{algorithm}: '{final_prefix}'")
            if "performance_summary" in result:
                perf = result["performance_summary"]
                print(f"  - Total time: {perf['total_execution_time_ms']}ms")
                print(f"  - Average time: {perf['average_execution_time_ms']}ms")
        else:
            print(f"{algorithm}: Error - {result['error']}")
    print()


def test_performance_metrics():
    """Test performance metrics functionality."""
    print("=" * 60)
    print("Testing Performance Metrics")
    print("=" * 60)
    
    tool = ProgressivePrefixFinderTool()
    
    test_strings = ["performance_test_string_1", "performance_test_string_2", "performance_test_different"]
    
    result = tool.forward(test_strings, algorithm="character", include_performance=True)
    
    print("Performance Data:")
    for perf in result["performance_data"]:
        print(f"Step {perf['step']}: {perf['execution_time_ms']}ms, {perf['memory_estimate']['estimated_bytes']} bytes")
    
    print(f"\nPerformance Summary:")
    summary = result["performance_summary"]
    for key, value in summary.items():
        print(f"{key}: {value}")
    print()


def test_usage_examples():
    """Test various usage examples."""
    print("=" * 60)
    print("Testing Usage Examples")
    print("=" * 60)
    
    tool = ProgressivePrefixFinderTool()
    
    # File paths
    file_paths = ["/home/user/documents/file1.txt", "/home/user/documents/file2.txt", "/home/user/downloads/file3.txt"]
    result = tool.forward(file_paths)
    print(f"File paths common prefix: '{result['summary']['final_common_prefix']}'")
    
    # URLs
    urls = ["https://example.com/api/v1/users", "https://example.com/api/v1/posts", "https://example.com/api/v2/users"]
    result = tool.forward(urls)
    print(f"URLs common prefix: '{result['summary']['final_common_prefix']}'")
    
    # Code patterns
    code_patterns = ["getUserData", "getUserInfo", "getUserProfile", "getPostData"]
    result = tool.forward(code_patterns)
    print(f"Code patterns common prefix: '{result['summary']['final_common_prefix']}'")
    
    print()


def test_examples_generator():
    """Test the usage examples generator."""
    print("=" * 60)
    print("Testing Examples Generator")
    print("=" * 60)
    
    examples = AdvancedPrefixAnalyzer.generate_usage_examples()
    
    print("Generated Usage Examples:")
    for category, example in examples.items():
        print(f"\n{category.upper()}:")
        print(f"  Description: {example.get('description', 'N/A')}")
        if 'input' in example:
            print(f"  Input: {example['input']}")
        if 'use_case' in example:
            print(f"  Use case: {example['use_case']}")
        if 'cases' in example:
            print(f"  Cases: {len(example['cases'])} test cases")
    print()


def main():
    """Run all tests."""
    print("Progressive Prefix Finder Tool - Test Suite")
    print("=" * 80)
    
    try:
        test_basic_functionality()
        test_edge_cases()
        test_algorithms_comparison()
        test_performance_metrics()
        test_usage_examples()
        test_examples_generator()
        
        print("=" * 80)
        print("All tests completed successfully!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())