# Progressive Common Prefix Finder Tool

## Overview

The Progressive Common Prefix Finder Tool is a powerful utility that finds common prefixes in a progressive way from a list of strings. It integrates seamlessly with the Hugging Face Smolagents framework and provides multiple algorithms for efficient prefix analysis.

## Features

### Core Functionality
- **Progressive Analysis**: Starts with first 2 strings, then adds one string at a time
- **Multiple Algorithms**: Character-by-character, binary search, and trie-based approaches
- **Performance Metrics**: Optional detailed performance and memory usage analysis
- **Edge Case Handling**: Robust handling of empty lists, single strings, and no common prefixes
- **Detailed Results**: Step-by-step breakdown of the progressive analysis process

### Supported Algorithms

1. **Character-by-Character** (`character`)
   - Simple and intuitive approach
   - Best for small to medium string lists
   - Time complexity: O(m × n) where m is minimum string length, n is number of strings

2. **Binary Search Optimization** (`binary_search`)
   - Uses binary search to find optimal prefix length
   - Efficient for longer strings with shorter common prefixes
   - Time complexity: O(m × log(m) × n)

3. **Trie-Based Approach** (`trie`)
   - Builds a trie structure for efficient prefix finding
   - Best for multiple strings with complex prefix patterns
   - Time complexity: O(m × n) with better space locality

## Usage Examples

### Basic Usage

```python
from tools.progressive_prefix_finder import ProgressivePrefixFinderTool

tool = ProgressivePrefixFinderTool()

# Basic example from problem statement
strings = ["prefix_test_1", "prefix_test_2", "prefix_demo", "prefix_example"]
result = tool.forward(strings)

print(f"Final common prefix: '{result['summary']['final_common_prefix']}'")
# Output: Final common prefix: 'prefix_'

# View progressive results
for step in result['results']:
    print(f"Step {step['step']}: {step['strings_count']} strings -> '{step['common_prefix']}'")
# Output:
# Step 1: 2 strings -> 'prefix_test_'
# Step 2: 3 strings -> 'prefix_'
# Step 3: 4 strings -> 'prefix_'
```

### Algorithm Comparison

```python
# Compare different algorithms
result_char = tool.forward(strings, algorithm="character", include_performance=True)
result_binary = tool.forward(strings, algorithm="binary_search", include_performance=True)
result_trie = tool.forward(strings, algorithm="trie", include_performance=True)

# All should produce the same result
assert result_char['summary']['final_common_prefix'] == result_binary['summary']['final_common_prefix']
```

### Performance Analysis

```python
result = tool.forward(strings, algorithm="character", include_performance=True)

# View performance summary
perf = result['performance_summary']
print(f"Total execution time: {perf['total_execution_time_ms']}ms")
print(f"Average execution time: {perf['average_execution_time_ms']}ms")
print(f"Peak memory estimate: {perf['peak_memory_estimate_bytes']} bytes")
```

### Advanced Analysis

```python
from tools.progressive_prefix_finder import AdvancedPrefixAnalyzer

# Compare all algorithms at once
comparison = AdvancedPrefixAnalyzer.compare_algorithms(strings, include_visualization=True)

# Get usage examples
examples = AdvancedPrefixAnalyzer.generate_usage_examples()
```

## Use Cases

### 1. File Path Analysis
```python
file_paths = [
    "/home/user/documents/file1.txt",
    "/home/user/documents/file2.txt", 
    "/home/user/downloads/file3.txt"
]
result = tool.forward(file_paths)
# Common path: "/home/user/do"
```

### 2. URL Prefix Extraction
```python
urls = [
    "https://example.com/api/v1/users",
    "https://example.com/api/v1/posts",
    "https://example.com/api/v2/users"
]
result = tool.forward(urls)
# Common prefix: "https://example.com/api/v"
```

### 3. Code Refactoring
```python
function_names = [
    "getUserData",
    "getUserInfo", 
    "getUserProfile",
    "getPostData"
]
result = tool.forward(function_names)
# Common prefix: "get"
```

## Output Format

### Standard Output
```json
{
    "results": [
        {
            "step": 1,
            "strings_count": 2,
            "common_prefix": "prefix_test_",
            "analyzed_strings": ["prefix_test_1", "prefix_test_2"]
        },
        {
            "step": 2,
            "strings_count": 3,
            "common_prefix": "prefix_",
            "analyzed_strings": ["prefix_test_1", "prefix_test_2", "prefix_demo"]
        }
    ],
    "total_steps": 2,
    "algorithm_used": "character",
    "summary": {
        "initial_strings_count": 3,
        "final_common_prefix": "prefix_",
        "prefix_length": 7
    }
}
```

### With Performance Metrics
```json
{
    "results": [...],
    "performance_data": [
        {
            "step": 1,
            "strings_count": 2,
            "execution_time_ms": 0.0131,
            "memory_estimate": {
                "input_chars": 26,
                "output_chars": 12,
                "strings_count": 2,
                "estimated_bytes": 152
            }
        }
    ],
    "performance_summary": {
        "total_execution_time_ms": 0.0225,
        "average_execution_time_ms": 0.0112,
        "max_execution_time_ms": 0.0131,
        "min_execution_time_ms": 0.0094,
        "peak_memory_estimate_bytes": 372,
        "total_strings_processed": 5
    }
}
```

## Edge Cases

The tool handles various edge cases gracefully:

- **Empty list**: Returns error message with empty results
- **Single string**: Returns the string itself as the common prefix
- **No common prefix**: Returns empty string as common prefix
- **Empty strings in list**: Properly handles empty strings in the input

## Performance Characteristics

### Character Algorithm
- **Best for**: Small to medium lists, short strings
- **Time**: O(m × n) where m = min string length, n = number of strings
- **Space**: O(1) additional space

### Binary Search Algorithm  
- **Best for**: Long strings with short common prefixes
- **Time**: O(m × log(m) × n)
- **Space**: O(1) additional space

### Trie Algorithm
- **Best for**: Complex prefix patterns, multiple analysis operations
- **Time**: O(m × n) for construction + O(m) for traversal
- **Space**: O(m × n) for trie storage

## Integration with Smolagents

The tool is fully integrated with the Smolagents framework:

1. **Tool Registration**: Added to `app.py` agent configuration
2. **Input Validation**: Follows Smolagents input/output specifications
3. **Error Handling**: Proper error responses for invalid inputs
4. **Type Safety**: Correct type annotations and validation

## Testing

Comprehensive test suite included:

- **Unit Tests**: `test_progressive_prefix.py` - Core functionality testing
- **Integration Tests**: `test_tool_integration.py` - Framework integration testing
- **Edge Case Tests**: Comprehensive edge case coverage
- **Performance Tests**: Algorithm performance comparison

Run tests with:
```bash
python test_progressive_prefix.py      # Full test suite
python test_tool_integration.py       # Integration tests only
```

## Installation

The tool is included in the repository and will be available when the agent is loaded. No additional installation required beyond the standard requirements.

## Contributing

When modifying the tool:

1. Maintain backward compatibility
2. Add appropriate tests for new features
3. Update documentation for any new functionality
4. Follow the existing code style and patterns
5. Ensure performance characteristics are maintained or improved