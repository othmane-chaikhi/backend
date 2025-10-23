"""
Google Gemini AI Service for Intelligent Code Correction
"""
import os
import json
from typing import Dict, Any, Optional
from django.conf import settings


class GeminiService:
    """Service to use Google Gemini AI for intelligent code correction"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini service
        
        Args:
            api_key: Google Gemini API key (or set GEMINI_API_KEY env var)
        """
        # Try to get API key from: parameter > Django settings > environment variable
        self.api_key = api_key or getattr(settings, 'GEMINI_API_KEY', '') or os.getenv('GEMINI_API_KEY', '')
        # Updated to use the latest Gemini model (gemini-2.5-flash is fast and accurate)
        self.model = "gemini-2.5-flash"
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        
        if not self.api_key:
            print("⚠️ Warning: GEMINI_API_KEY not set. AI correction disabled.")
        else:
            print(f"✅ Gemini AI enabled ({self.model}) with API key: {self.api_key[:20]}...")
    
    def is_available(self) -> bool:
        """Check if Gemini API is available"""
        return bool(self.api_key)
    
    def evaluate_code(
        self,
        submitted_code: str,
        solution_code: str,
        language: str,
        instructions: str,
        execution_output: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Use Gemini AI to intelligently evaluate submitted code
        
        Args:
            submitted_code: The code submitted by the user
            solution_code: The expected solution code
            language: Programming language (python, java, cpp, etc.)
            instructions: Exercise instructions
            execution_output: Output from Judge0 execution (if available)
        
        Returns:
            Dict with evaluation results:
            {
                'is_correct': bool,
                'score': int (0-100),
                'feedback': str,
                'suggestions': str,
                'accepts_alternative': bool
            }
        """
        if not self.is_available():
            # Fallback to basic validation if Gemini not available
            return self._basic_validation(submitted_code, solution_code, execution_output)
        
        try:
            import requests
            
            # Build the prompt for Gemini
            prompt = self._build_evaluation_prompt(
                submitted_code,
                solution_code,
                language,
                instructions,
                execution_output
            )
            
            # Call Gemini API
            headers = {
                'Content-Type': 'application/json',
            }
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.2,  # Lower temperature for more consistent evaluation
                    "topK": 1,
                    "topP": 0.95,
                    "maxOutputTokens": 2048,
                    "responseMimeType": "application/json"  # Force JSON response
                }
            }
            
            url = f"{self.base_url}?key={self.api_key}"
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code != 200:
                print(f"Gemini API error: {response.status_code} - {response.text}")
                return self._basic_validation(submitted_code, solution_code, execution_output)
            
            result = response.json()
            
            # Parse Gemini response
            return self._parse_gemini_response(result)
            
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return self._basic_validation(submitted_code, solution_code, execution_output)
    
    def _build_evaluation_prompt(
        self,
        submitted_code: str,
        solution_code: str,
        language: str,
        instructions: str,
        execution_output: Optional[str]
    ) -> str:
        """Build a detailed prompt for Gemini to evaluate the code"""
        
        prompt = f"""You are an expert programming teacher evaluating student code.

**Exercise Instructions:**
{instructions}

**Programming Language:** {language}

**Expected Solution:**
```{language}
{solution_code}
```

**Student's Submitted Code:**
```{language}
{submitted_code}
```
"""
        
        if execution_output:
            prompt += f"""
**Execution Output:**
{execution_output}

**Note:** If the code uses browser-specific APIs (alert, prompt, document, etc.) and failed to execute in Node.js, 
this is NORMAL. Focus on evaluating the code LOGIC and CORRECTNESS, not the execution result.
"""
        
        prompt += """
**Your Task:**
Evaluate if the student's code is correct. Consider:
1. Does it solve the problem correctly?
2. Is the logic sound?
3. Does it produce the correct output?
4. Accept alternative correct solutions (different approaches that work)

**IMPORTANT:** Be flexible! If the student used a different but valid approach, accept it!

**CRITICAL: You MUST respond with ONLY a valid JSON object, nothing else. No markdown, no explanations, just pure JSON.**

**Response Format:**
{
  "is_correct": true,
  "score": 95,
  "feedback": "Brief feedback message (1-2 sentences)",
  "suggestions": "Improvement suggestions (if any)",
  "accepts_alternative": true,
  "reasoning": "Why you marked it correct/incorrect"
}

Return ONLY the JSON object above. Do not wrap it in code blocks or add any other text.
"""
        
        return prompt
    
    def _parse_gemini_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Gemini API response and extract evaluation"""
        try:
            # Extract text from Gemini response
            if 'candidates' in response and len(response['candidates']) > 0:
                candidate = response['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    text = candidate['content']['parts'][0]['text']
                    
                    # Log the raw response for debugging
                    print(f"🔍 AI Response (first 300 chars): {text[:300]}")
                    
                    # Try to parse as JSON
                    # Remove markdown code blocks if present
                    text = text.strip()
                    
                    # More aggressive cleaning of markdown blocks
                    import re
                    # Extract JSON from markdown code blocks
                    json_match = re.search(r'```(?:json|JSON)?\s*(\{.*?\})\s*```', text, re.DOTALL)
                    if json_match:
                        text = json_match.group(1)
                    elif text.startswith('```'):
                        # Remove ```json, ```JSON, or ``` markers
                        text = text.replace('```json', '').replace('```JSON', '').replace('```', '').strip()
                    
                    # Try to extract just the JSON object if there's extra text
                    json_match = re.search(r'\{[^}]*"is_correct"[^}]*\}', text, re.DOTALL)
                    if json_match:
                        text = json_match.group(0)
                    
                    try:
                        result = json.loads(text)
                        
                        # Ensure required fields
                        return {
                            'is_correct': result.get('is_correct', False),
                            'score': result.get('score', 0),
                            'feedback': result.get('feedback', 'Code evaluated by AI'),
                            'suggestions': result.get('suggestions', ''),
                            'accepts_alternative': result.get('accepts_alternative', False),
                            'reasoning': result.get('reasoning', '')
                        }
                    except json.JSONDecodeError as je:
                        # If JSON parsing fails, log and try to extract info from text
                        print(f"⚠️ JSON parsing failed: {je}")
                        print(f"📝 Text that failed to parse: {text[:500]}")
                        
                        is_correct = 'correct' in text.lower() and 'incorrect' not in text.lower()
                        
                        # Try to extract feedback from the text
                        feedback_match = re.search(r'"feedback"\s*:\s*"([^"]+)"', text)
                        feedback = feedback_match.group(1) if feedback_match else text[:200]
                        
                        return {
                            'is_correct': is_correct,
                            'score': 100 if is_correct else 50,
                            'feedback': feedback,
                            'suggestions': 'Please review the code logic',
                            'accepts_alternative': False,
                            'reasoning': text[:300]
                        }
            
            # Log when response structure is unexpected
            print(f"⚠️ Unexpected response structure: {json.dumps(response, indent=2)[:500]}")
            
            return {
                'is_correct': False,
                'score': 0,
                'feedback': 'Could not parse AI response. Using fallback evaluation.',
                'suggestions': 'The AI service returned an unexpected format. Your code is being evaluated with basic logic.',
                'accepts_alternative': False,
                'reasoning': 'Parse error: Response structure unexpected'
            }
            
        except Exception as e:
            print(f"❌ Error parsing Gemini response: {e}")
            import traceback
            traceback.print_exc()
            return {
                'is_correct': False,
                'score': 0,
                'feedback': 'Error evaluating code with AI',
                'suggestions': 'There was an error processing the AI response. Please try again.',
                'accepts_alternative': False,
                'reasoning': str(e)
            }
    
    def _basic_validation(
        self,
        submitted_code: str,
        solution_code: str,
        execution_output: Optional[str]
    ) -> Dict[str, Any]:
        """
        Basic validation fallback when Gemini is not available
        Just checks if code is similar to solution
        """
        submitted_clean = ''.join(submitted_code.split()).lower()
        solution_clean = ''.join(solution_code.split()).lower()
        
        # Simple similarity check
        if len(submitted_clean) < 10:
            return {
                'is_correct': False,
                'score': 0,
                'feedback': 'Code too short. Please write a complete solution.',
                'suggestions': 'Write more code based on the instructions.',
                'accepts_alternative': False,
                'reasoning': 'Code length insufficient'
            }
        
        # Check similarity
        similarity = self._calculate_similarity(submitted_clean, solution_clean)
        
        if similarity > 0.7:
            return {
                'is_correct': True,
                'score': int(similarity * 100),
                'feedback': 'Your solution looks correct!',
                'suggestions': '',
                'accepts_alternative': True,
                'reasoning': f'Similarity: {similarity:.2f}'
            }
        else:
            return {
                'is_correct': False,
                'score': int(similarity * 100),
                'feedback': 'Your solution needs improvement.',
                'suggestions': 'Compare your code with the expected solution.',
                'accepts_alternative': False,
                'reasoning': f'Similarity too low: {similarity:.2f}'
            }
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate simple similarity between two strings"""
        if not text1 or not text2:
            return 0.0
        
        # Simple character-level similarity
        common = sum(1 for a, b in zip(text1, text2) if a == b)
        max_len = max(len(text1), len(text2))
        
        return common / max_len if max_len > 0 else 0.0


# Singleton instance
_gemini_service = None

def get_gemini_service() -> GeminiService:
    """Get or create Gemini service instance"""
    global _gemini_service
    if _gemini_service is None:
        _gemini_service = GeminiService()
    return _gemini_service

