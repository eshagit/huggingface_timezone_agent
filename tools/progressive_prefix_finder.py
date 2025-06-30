from typing import Any, List, Dict, Optional
from smolagents.tools import Tool
import time
from collections import defaultdict


class ProgressivePrefixFinderTool(Tool):
    name = "progressive_prefix_finder"
    description = "Finds common prefixes progressively from a list of strings. Starts with first 2 strings, then adds one at a time until all strings are processed."
    inputs = {
        'strings': {'type': 'array', 'description': 'List of strings to analyze for common prefixes'},
        'algorithm': {'type': 'string', 'description': 'Algorithm to use: "character", "binary_search", or "trie" (default: "character")', 'nullable': True},
        'include_performance': {'type': 'boolean', 'description': 'Whether to include performance metrics (default: False)', 'nullable': True}
    }
    output_type = "object"

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.is_initialized = True

    def forward(self, strings: List[str], algorithm: str = "character", include_performance: bool = False) -> Dict[str, Any]:
        """
        Find common prefixes progressively using the specified algorithm.
        
        Args:
            strings: List of strings to analyze
            algorithm: Algorithm to use ("character", "binary_search", "trie")
            include_performance: Whether to include performance metrics
            
        Returns:
            Dictionary containing progressive results and optional performance data
        """
        if not strings:
            return {"error": "Empty string list provided", "results": []}
        
        if len(strings) == 1:
            return {
                "results": [{"step": 1, "strings_count": 1, "common_prefix": strings[0], "analyzed_strings": strings}],
                "total_steps": 1,
                "algorithm_used": algorithm,
                "summary": {
                    "initial_strings_count": 1,
                    "final_common_prefix": strings[0],
                    "prefix_length": len(strings[0])
                }
            }
        
        # Choose algorithm
        if algorithm == "character":
            finder_func = self._find_common_prefix_character
        elif algorithm == "binary_search":
            finder_func = self._find_common_prefix_binary_search
        elif algorithm == "trie":
            finder_func = self._find_common_prefix_trie
        else:
            return {"error": f"Unknown algorithm: {algorithm}", "results": []}
        
        results = []
        performance_data = [] if include_performance else None
        
        # Progressive analysis: start with 2 strings, then 3, 4, etc.
        for i in range(2, len(strings) + 1):
            current_strings = strings[:i]
            
            if include_performance:
                start_time = time.perf_counter()
                common_prefix = finder_func(current_strings)
                end_time = time.perf_counter()
                
                performance_data.append({
                    "step": i - 1,
                    "strings_count": i,
                    "execution_time_ms": round((end_time - start_time) * 1000, 4),
                    "memory_estimate": self._estimate_memory_usage(current_strings, common_prefix)
                })
            else:
                common_prefix = finder_func(current_strings)
            
            results.append({
                "step": i - 1,
                "strings_count": i,
                "common_prefix": common_prefix,
                "analyzed_strings": current_strings[:3] + (["..."] if len(current_strings) > 3 else [])
            })
        
        response = {
            "results": results,
            "total_steps": len(results),
            "algorithm_used": algorithm,
            "summary": {
                "initial_strings_count": len(strings),
                "final_common_prefix": results[-1]["common_prefix"] if results else "",
                "prefix_length": len(results[-1]["common_prefix"]) if results else 0
            }
        }
        
        if include_performance:
            response["performance_data"] = performance_data
            response["performance_summary"] = self._summarize_performance(performance_data)
        
        return response

    def _find_common_prefix_character(self, strings: List[str]) -> str:
        """Character-by-character comparison algorithm."""
        if not strings:
            return ""
        
        if len(strings) == 1:
            return strings[0]
        
        # Find the minimum length to avoid index errors
        min_length = min(len(s) for s in strings)
        common_prefix = ""
        
        for i in range(min_length):
            char = strings[0][i]
            if all(s[i] == char for s in strings):
                common_prefix += char
            else:
                break
        
        return common_prefix

    def _find_common_prefix_binary_search(self, strings: List[str]) -> str:
        """Binary search optimization algorithm."""
        if not strings:
            return ""
        
        if len(strings) == 1:
            return strings[0]
        
        min_length = min(len(s) for s in strings)
        
        def is_common_prefix(length: int) -> bool:
            if length == 0:
                return True
            prefix = strings[0][:length]
            return all(s.startswith(prefix) for s in strings)
        
        # Binary search for the longest common prefix length
        left, right = 0, min_length
        while left < right:
            mid = (left + right + 1) // 2
            if is_common_prefix(mid):
                left = mid
            else:
                right = mid - 1
        
        return strings[0][:left]

    def _find_common_prefix_trie(self, strings: List[str]) -> str:
        """Trie-based approach for multiple strings."""
        if not strings:
            return ""
        
        if len(strings) == 1:
            return strings[0]
        
        # Build trie
        trie = {}
        for string in strings:
            node = trie
            for char in string:
                if char not in node:
                    node[char] = {}
                node = node[char]
            node['$'] = True  # End of string marker
        
        # Find common prefix by traversing trie
        common_prefix = ""
        node = trie
        
        while len(node) == 1 and '$' not in node:
            char = next(iter(node.keys()))
            common_prefix += char
            node = node[char]
        
        return common_prefix

    def _estimate_memory_usage(self, strings: List[str], prefix: str) -> Dict[str, int]:
        """Estimate memory usage for the operation."""
        input_size = sum(len(s) for s in strings)
        output_size = len(prefix)
        
        return {
            "input_chars": input_size,
            "output_chars": output_size,
            "strings_count": len(strings),
            "estimated_bytes": input_size * 4 + output_size * 4  # Rough estimate for Unicode strings
        }

    def _summarize_performance(self, performance_data: List[Dict]) -> Dict[str, Any]:
        """Summarize performance metrics."""
        if not performance_data:
            return {}
        
        execution_times = [p["execution_time_ms"] for p in performance_data]
        memory_estimates = [p["memory_estimate"]["estimated_bytes"] for p in performance_data]
        
        return {
            "total_execution_time_ms": round(sum(execution_times), 4),
            "average_execution_time_ms": round(sum(execution_times) / len(execution_times), 4),
            "max_execution_time_ms": round(max(execution_times), 4),
            "min_execution_time_ms": round(min(execution_times), 4),
            "peak_memory_estimate_bytes": max(memory_estimates),
            "total_strings_processed": sum(p["strings_count"] for p in performance_data)
        }


class AdvancedPrefixAnalyzer:
    """Advanced utilities for prefix analysis and visualization."""
    
    @staticmethod
    def compare_algorithms(strings: List[str], include_visualization: bool = False) -> Dict[str, Any]:
        """Compare performance of different algorithms."""
        tool = ProgressivePrefixFinderTool()
        algorithms = ["character", "binary_search", "trie"]
        
        results = {}
        for algorithm in algorithms:
            try:
                result = tool.forward(strings, algorithm=algorithm, include_performance=True)
                results[algorithm] = result
            except Exception as e:
                results[algorithm] = {"error": str(e)}
        
        # Create comparison summary
        comparison = {
            "algorithms_compared": algorithms,
            "input_strings_count": len(strings),
            "comparison_results": results
        }
        
        if include_visualization:
            comparison["visualization"] = AdvancedPrefixAnalyzer._create_visualization_data(results)
        
        return comparison
    
    @staticmethod
    def _create_visualization_data(results: Dict[str, Any]) -> Dict[str, Any]:
        """Create data for visualization of algorithm performance."""
        viz_data = {
            "performance_chart": {},
            "memory_usage": {},
            "accuracy_check": {}
        }
        
        for algorithm, result in results.items():
            if "error" not in result and "performance_data" in result:
                perf_data = result["performance_data"]
                viz_data["performance_chart"][algorithm] = [
                    {"step": p["step"], "time_ms": p["execution_time_ms"]} 
                    for p in perf_data
                ]
                viz_data["memory_usage"][algorithm] = [
                    {"step": p["step"], "memory_bytes": p["memory_estimate"]["estimated_bytes"]} 
                    for p in perf_data
                ]
                
                # Check if all algorithms produce the same result
                final_prefix = result["summary"]["final_common_prefix"]
                viz_data["accuracy_check"][algorithm] = final_prefix
        
        return viz_data
    
    @staticmethod
    def generate_usage_examples() -> Dict[str, Any]:
        """Generate comprehensive usage examples."""
        examples = {
            "basic_usage": {
                "description": "Basic progressive prefix finding",
                "input": ["prefix_test_1", "prefix_test_2", "prefix_demo", "prefix_example"],
                "expected_output": "Progressive analysis finding common prefixes"
            },
            "file_paths": {
                "description": "Finding common directory paths",
                "input": ["/home/user/documents/file1.txt", "/home/user/documents/file2.txt", "/home/user/downloads/file3.txt"],
                "use_case": "File path analysis"
            },
            "urls": {
                "description": "URL prefix extraction",
                "input": ["https://example.com/api/v1/users", "https://example.com/api/v1/posts", "https://example.com/api/v2/users"],
                "use_case": "Web crawling and analysis"
            },
            "code_patterns": {
                "description": "Identifying common naming patterns",
                "input": ["getUserData", "getUserInfo", "getUserProfile", "getPostData"],
                "use_case": "Code refactoring"
            },
            "edge_cases": {
                "description": "Edge case handling",
                "cases": [
                    {"input": [], "description": "Empty list"},
                    {"input": ["single"], "description": "Single string"},
                    {"input": ["abc", "xyz"], "description": "No common prefix"},
                    {"input": ["", "abc"], "description": "Empty string in list"}
                ]
            }
        }
        
        return examples