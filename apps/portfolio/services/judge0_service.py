"""
Judge0 API Service for executing code in multiple languages
"""
import time
from typing import Dict, Any, Optional

try:
    import requests
except ImportError:
    requests = None
    print("⚠️ requests module not found. Install with: pip install requests")


# Judge0 Community Free Endpoint
JUDGE0_FREE_URL = "https://ce.judge0.com"

# Language ID mapping (Judge0 language IDs)
LANGUAGE_IDS = {
    'python': 71,      # Python 3.8.1
    'javascript': 63,  # JavaScript (Node.js 12.14.0)
    'java': 62,        # Java (OpenJDK 13.0.1)
    'cpp': 54,         # C++ (GCC 9.2.0)
    'c': 50,           # C (GCC 9.2.0)
    'sql': 82,         # SQL (SQLite 3.27.2)
    'html': 63,        # Use JavaScript for HTML/CSS/JS combo
    'typescript': 74,  # TypeScript (3.7.4)
}


class Judge0Service:
    """Service to interact with Judge0 API"""
    
    def __init__(self):
        """
        Initialize Judge0 service with free community endpoint
        """
        self.base_url = JUDGE0_FREE_URL
        self.headers = {
            "Content-Type": "application/json"
        }
        
        if requests is None:
            print("⚠️ Warning: requests module not available. Judge0 execution disabled.")
    
    def is_available(self) -> bool:
        """Check if Judge0 service is available"""
        return requests is not None
    
    def execute_code(
        self,
        source_code: str,
        language: str,
        stdin: str = "",
        expected_output: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute code using Judge0 API
        
        Args:
            source_code: The source code to execute
            language: Programming language ('python', 'java', 'cpp', etc.)
            stdin: Standard input for the program
            expected_output: Expected output for validation
        
        Returns:
            Dict with execution results:
            {
                'success': bool,
                'stdout': str,
                'stderr': str,
                'status': str,
                'time': float,
                'memory': int,
                'compile_output': str,
                'message': str
            }
        """
        # Check if requests is available
        if not self.is_available():
            return {
                'success': False,
                'error': 'Judge0 service not available (requests module missing)',
                'message': '⚠️ Judge0 execution not available. Install: pip install requests'
            }
        
        try:
            # Get language ID
            language_id = LANGUAGE_IDS.get(language)
            if not language_id:
                return {
                    'success': False,
                    'error': f'Language "{language}" not supported by Judge0',
                    'message': f'❌ Language "{language}" not supported'
                }
            
            # Create submission
            submission_data = {
                "source_code": source_code,
                "language_id": language_id,
                "stdin": stdin
            }
            
            # Only add expected_output if provided
            if expected_output:
                submission_data["expected_output"] = expected_output
            
            # Submit code
            try:
                response = requests.post(
                    f"{self.base_url}/submissions",
                    params={"base64_encoded": "false", "wait": "false"},
                    json=submission_data,
                    headers=self.headers,
                    timeout=15
                )
            except requests.exceptions.Timeout:
                return {
                    'success': False,
                    'error': 'Judge0 request timeout',
                    'message': '⏱️ Request timeout. Judge0 server might be slow. Try again.'
                }
            except requests.exceptions.ConnectionError:
                return {
                    'success': False,
                    'error': 'Cannot connect to Judge0',
                    'message': '🌐 Cannot connect to Judge0. Check your internet connection.'
                }
            
            if response.status_code not in [200, 201]:
                error_detail = response.text[:200] if response.text else 'Unknown error'
                return {
                    'success': False,
                    'error': f'Submission failed: {response.status_code}',
                    'message': f'❌ Judge0 error: {error_detail}'
                }
            
            submission = response.json()
            token = submission.get('token')
            
            if not token:
                return {
                    'success': False,
                    'error': 'No submission token received',
                    'message': 'Submission error'
                }
            
            # Wait for result (polling)
            result = self._wait_for_result(token)
            return result
            
        except requests.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'🌐 Network error: {str(e)[:100]}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'❌ Unexpected error: {str(e)[:100]}'
            }
    
    def _wait_for_result(self, token: str, max_attempts: int = 10) -> Dict[str, Any]:
        """
        Poll Judge0 API for submission result
        
        Args:
            token: Submission token
            max_attempts: Maximum number of polling attempts
        
        Returns:
            Dict with execution results
        """
        for attempt in range(max_attempts):
            try:
                response = requests.get(
                    f"{self.base_url}/submissions/{token}",
                    params={"base64_encoded": "false"},
                    headers=self.headers,
                    timeout=10
                )
                
                if response.status_code != 200:
                    time.sleep(1)
                    continue
                
                result = response.json()
                status_id = result.get('status', {}).get('id')
                
                # Status IDs:
                # 1: In Queue
                # 2: Processing
                # 3: Accepted
                # 4: Wrong Answer
                # 5: Time Limit Exceeded
                # 6: Compilation Error
                # 7-14: Various runtime errors
                
                if status_id in [1, 2]:  # Still processing
                    time.sleep(1)
                    continue
                
                # Process completed
                return self._format_result(result)
                
            except requests.RequestException:
                time.sleep(1)
                continue
        
        return {
            'success': False,
            'error': 'Execution timeout',
            'message': 'Code execution took too long'
        }
    
    def _format_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format Judge0 result into a standardized response
        
        Args:
            result: Raw Judge0 result
        
        Returns:
            Formatted result dict
        """
        status = result.get('status', {})
        if not status:
            status = {}
        
        status_id = status.get('id')
        status_description = status.get('description', 'Unknown')
        
        # Safely get and strip strings (handle None values)
        stdout = (result.get('stdout') or '').strip()
        stderr = (result.get('stderr') or '').strip()
        compile_output = (result.get('compile_output') or '').strip()
        time_taken = result.get('time') or 0
        memory_used = result.get('memory') or 0
        
        # Determine success
        success = status_id == 3  # Accepted
        
        # Build message
        if status_id == 3:
            message = '✅ Code executed successfully!'
        elif status_id == 6:
            message = '❌ Compilation Error'
        elif status_id == 4:
            message = '❌ Wrong Answer'
        elif status_id == 5:
            message = '❌ Time Limit Exceeded'
        elif status_id in [7, 8, 9, 10, 11, 12, 13, 14]:
            message = f'❌ Runtime Error: {status_description}'
        else:
            message = f'⚠️ {status_description}'
        
        return {
            'success': success,
            'status': status_description,
            'status_id': status_id,
            'stdout': stdout,
            'stderr': stderr,
            'compile_output': compile_output,
            'time': time_taken,
            'memory': memory_used,
            'message': message
        }
    
    def validate_solution(
        self,
        source_code: str,
        language: str,
        expected_output: str,
        stdin: str = ""
    ) -> Dict[str, Any]:
        """
        Execute code and validate against expected output
        
        Args:
            source_code: The source code to execute
            language: Programming language
            expected_output: Expected output for validation
            stdin: Standard input for the program
        
        Returns:
            Dict with validation results
        """
        result = self.execute_code(source_code, language, stdin, expected_output)
        
        if not result.get('success'):
            return result
        
        # Check if output matches expected
        actual_output = result.get('stdout', '').strip()
        expected = expected_output.strip()
        
        if actual_output == expected:
            result['validated'] = True
            result['message'] = '✅ Correct! Your solution produces the expected output.'
        else:
            result['validated'] = False
            result['message'] = '❌ Incorrect output'
            result['expected_output'] = expected
            result['actual_output'] = actual_output
        
        return result


# Singleton instance
_judge0_service = None

def get_judge0_service() -> Judge0Service:
    """Get or create Judge0 service instance"""
    global _judge0_service
    if _judge0_service is None:
        _judge0_service = Judge0Service()  # Use free endpoint
    return _judge0_service

