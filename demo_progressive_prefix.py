#!/usr/bin/env python3
"""
Demonstration script for the Progressive Prefix Finder Tool
Shows how the tool works with various real-world examples
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.progressive_prefix_finder import ProgressivePrefixFinderTool, AdvancedPrefixAnalyzer


def demo_basic_usage():
    """Demonstrate basic progressive prefix finding."""
    print("🔍 Basic Progressive Prefix Finding")
    print("=" * 50)
    
    tool = ProgressivePrefixFinderTool()
    
    # Example from problem statement
    strings = ["prefix_test_1", "prefix_test_2", "prefix_demo", "prefix_example"]
    print(f"Input strings: {strings}")
    
    result = tool.forward(strings)
    
    print("\nProgressive Results:")
    for step in result['results']:
        analyzed = step['analyzed_strings']
        if '...' in analyzed:
            analyzed_str = f"{analyzed[:-1]} + {step['strings_count'] - len(analyzed) + 1} more"
        else:
            analyzed_str = str(analyzed)
        print(f"  Step {step['step']}: {analyzed_str}")
        print(f"    → Common prefix: '{step['common_prefix']}'")
    
    print(f"\n✅ Final Result: '{result['summary']['final_common_prefix']}' (length: {result['summary']['prefix_length']})")
    print()


def demo_real_world_examples():
    """Show real-world use cases."""
    print("🌍 Real-World Use Cases")
    print("=" * 50)
    
    tool = ProgressivePrefixFinderTool()
    
    examples = [
        {
            "name": "File Paths",
            "description": "Finding common directory structures",
            "strings": [
                "/home/user/projects/web-app/src/components/Button.js",
                "/home/user/projects/web-app/src/components/Modal.js",
                "/home/user/projects/web-app/src/utils/helpers.js",
                "/home/user/projects/mobile-app/src/screens/Home.js"
            ]
        },
        {
            "name": "API Endpoints",
            "description": "Identifying common URL patterns",
            "strings": [
                "https://api.example.com/v1/users/123/profile",
                "https://api.example.com/v1/users/456/settings",
                "https://api.example.com/v1/posts/789/comments",
                "https://api.example.com/v2/users/101/profile"
            ]
        },
        {
            "name": "Function Names",
            "description": "Code refactoring and pattern detection",
            "strings": [
                "calculateUserScore",
                "calculateTeamScore", 
                "calculateGameScore",
                "validateUserInput"
            ]
        },
        {
            "name": "Database Tables",
            "description": "Database schema analysis",
            "strings": [
                "user_profile_data",
                "user_login_history",
                "user_preferences",
                "admin_user_management"
            ]
        }
    ]
    
    for example in examples:
        print(f"\n📁 {example['name']}")
        print(f"   {example['description']}")
        print(f"   Input: {len(example['strings'])} strings")
        
        result = tool.forward(example['strings'])
        final_prefix = result['summary']['final_common_prefix']
        
        if final_prefix:
            print(f"   ✅ Common prefix: '{final_prefix}' (length: {len(final_prefix)})")
        else:
            print(f"   ❌ No common prefix found")
        
        # Show progression for interesting cases
        if len(final_prefix) > 5:  # Only show progression for meaningful prefixes
            print("   📈 Progression:")
            for step in result['results']:
                if step['step'] <= 3:  # Show first few steps
                    print(f"      Step {step['step']}: '{step['common_prefix']}'")
    print()


def demo_algorithm_comparison():
    """Compare different algorithms."""
    print("⚡ Algorithm Performance Comparison")
    print("=" * 50)
    
    # Use a larger dataset for meaningful comparison
    test_strings = [
        "performance_benchmark_test_string_number_001_with_long_suffix",
        "performance_benchmark_test_string_number_002_with_long_suffix", 
        "performance_benchmark_test_string_number_003_with_long_suffix",
        "performance_benchmark_test_different_pattern_004",
        "performance_benchmark_analysis_005"
    ]
    
    print(f"Test dataset: {len(test_strings)} strings")
    print(f"Average length: {sum(len(s) for s in test_strings) // len(test_strings)} characters")
    
    comparison = AdvancedPrefixAnalyzer.compare_algorithms(test_strings, include_visualization=True)
    
    print("\n📊 Results by Algorithm:")
    for algorithm, result in comparison["comparison_results"].items():
        if "error" not in result:
            prefix = result["summary"]["final_common_prefix"]
            perf = result.get("performance_summary", {})
            
            print(f"\n  {algorithm.upper()}:")
            print(f"    Result: '{prefix}' (length: {len(prefix)})")
            if perf:
                print(f"    Total time: {perf.get('total_execution_time_ms', 0):.4f}ms")
                print(f"    Average time: {perf.get('average_execution_time_ms', 0):.4f}ms")
                print(f"    Peak memory: {perf.get('peak_memory_estimate_bytes', 0)} bytes")
        else:
            print(f"  {algorithm.upper()}: ERROR - {result['error']}")
    
    # Verify all algorithms produce same result
    results = [r["summary"]["final_common_prefix"] for r in comparison["comparison_results"].values() if "error" not in r]
    if len(set(results)) == 1:
        print(f"\n✅ All algorithms produced identical results: '{results[0]}'")
    else:
        print(f"\n❌ Algorithms produced different results: {results}")
    print()


def demo_edge_cases():
    """Demonstrate edge case handling."""
    print("🔧 Edge Case Handling")
    print("=" * 50)
    
    tool = ProgressivePrefixFinderTool()
    
    test_cases = [
        {
            "name": "Empty List",
            "input": [],
            "expected": "Error handling"
        },
        {
            "name": "Single String", 
            "input": ["lonely_string"],
            "expected": "Returns the string itself"
        },
        {
            "name": "No Common Prefix",
            "input": ["apple", "banana", "cherry"],
            "expected": "Empty common prefix"
        },
        {
            "name": "Empty String in List",
            "input": ["", "hello", "help"],
            "expected": "Empty common prefix"
        },
        {
            "name": "Identical Strings",
            "input": ["same", "same", "same"],
            "expected": "Full string as prefix"
        },
        {
            "name": "One Character Difference",
            "input": ["test1", "test2", "test3"],
            "expected": "Prefix up to difference"
        }
    ]
    
    for case in test_cases:
        print(f"\n🧪 {case['name']}")
        print(f"   Input: {case['input']}")
        print(f"   Expected: {case['expected']}")
        
        result = tool.forward(case['input'])
        
        if "error" in result:
            print(f"   ✅ Result: {result['error']}")
        else:
            final_prefix = result['summary']['final_common_prefix']
            print(f"   ✅ Result: '{final_prefix}' (length: {len(final_prefix)})")
    print()


def demo_performance_analysis():
    """Show detailed performance analysis."""
    print("📈 Performance Analysis")
    print("=" * 50)
    
    tool = ProgressivePrefixFinderTool()
    
    # Create progressively larger datasets
    base_strings = ["performance_test_prefix_", "performance_test_different_", "performance_analysis_"]
    
    for size in [5, 10, 15]:
        test_strings = []
        for i in range(size):
            base = base_strings[i % len(base_strings)]
            test_strings.append(f"{base}string_{i:03d}")
        
        print(f"\n📊 Dataset size: {size} strings")
        
        result = tool.forward(test_strings, algorithm="character", include_performance=True)
        perf = result["performance_summary"]
        
        print(f"   Final prefix: '{result['summary']['final_common_prefix']}'")
        print(f"   Total time: {perf['total_execution_time_ms']:.4f}ms")
        print(f"   Average per step: {perf['average_execution_time_ms']:.4f}ms")
        print(f"   Peak memory: {perf['peak_memory_estimate_bytes']} bytes")
        print(f"   Steps completed: {result['total_steps']}")
    print()


def main():
    """Run all demonstrations."""
    print("🚀 Progressive Prefix Finder Tool - Demonstration")
    print("=" * 80)
    print("This tool finds common prefixes progressively from a list of strings.")
    print("It supports multiple algorithms and provides detailed analysis.\n")
    
    try:
        demo_basic_usage()
        demo_real_world_examples()
        demo_algorithm_comparison()
        demo_edge_cases()
        demo_performance_analysis()
        
        print("=" * 80)
        print("🎉 Demonstration completed successfully!")
        print("\nThe Progressive Prefix Finder Tool is ready for use in the agent.")
        print("It can be accessed through the agent interface with the name 'progressive_prefix_finder'.")
        
    except Exception as e:
        print(f"❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())