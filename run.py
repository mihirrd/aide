import os
import dotenv
import json
from typing import Dict, List, Any
from openai import OpenAI
from dataclasses import dataclass


@dataclass
class CodeChallenge:
    """Data class to store challenge details"""
    code: str
    concept: str
    difficulty: str

@dataclass
class EvaluationResult:
    """Data class to store evaluation results"""
    score: int
    improvements: List[str]
    suggestions: List[str]
    explanation: str
    

class OpenAIProvider():
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def generate_challenge(self, concept: str, difficulty: str) -> CodeChallenge:
        prompt = f"""Create a Python code snippet about {concept} at {difficulty} level that has:
        1. Contains 2-3 bugs that a student should be able to identify
        2. Has inconsistent naming issues
        3. Could be improved for better readability
        4. Is between 15-20 lines of code
        
        Return only the code without any explanations."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a coding instructor creating practice exercises."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return CodeChallenge(
            code=response.choices[0].message.content.strip(),
            concept=concept,
            difficulty=difficulty
        )
        
    def _create_evaluation_prompt(self, original_code: str, user_solution: str) -> str:
        """Create a standardized evaluation prompt"""
        return f"""Compare the original buggy code and the user's solution:
        
        Original code:
        {original_code}
        
        User's solution:
        {user_solution}
        
        Provide an evaluation in the following JSON format:
        {{
            "score": <number between 0-100>,
            "improvements": [<improvements made by the user in the original code>],
            "suggestions": [<list of potential further improvements>],
            "explanation": "<brief explanation of the score>"
        }}
        
        Base the score on:
        - Bug fixes (40 points)
        - Code style improvements (30 points)
        - Code efficiency/readability (30 points)
        
        Ensure the response is valid JSON."""
    
    def evaluate_solution(self, original_code: str, user_solution: str) -> EvaluationResult:
        prompt = self._create_evaluation_prompt(original_code, user_solution)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a coding instructor evaluating student solutions."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }  # Changed from "json" to "json_object"
        )
        
        result = json.loads(response.choices[0].message.content)
        return EvaluationResult(**result)


class CodePracticeTool:
    def __init__(self, provider: OpenAIProvider):
        self.provider = provider
        self.programming_concepts = [
            "list comprehension", "error handling", "file handling",
            "class implementation", "data processing", "sorting algorithm",
            "recursive function", "decorator implementation", "API interaction",
            "database operations"
        ]
        self.difficulty_levels = ["beginner", "intermediate", "advanced"]
    
    def run_practice_session(self):
        """Run an interactive practice session"""
        print("Welcome to Code Coach AI!")
        
        # Let user choose concept and difficulty
        print("\nAvailable concepts:")
        for i, concept in enumerate(self.programming_concepts, 1):
            print(f"{i}. {concept}")
        
        concept_idx = int(input("\nChoose a concept (enter number): ")) - 1
        concept = self.programming_concepts[concept_idx]
        
        print("\nDifficulty levels:")
        for i, level in enumerate(self.difficulty_levels, 1):
            print(f"{i}. {level}")
        
        difficulty_idx = int(input("\nChoose difficulty (enter number): ")) - 1
        difficulty = self.difficulty_levels[difficulty_idx]
        
        try:
            # Generate challenge
            print("\nGenerating challenge...")
            challenge = self.provider.generate_challenge(concept, difficulty)
            
            print(f"\nHere's a {difficulty} level challenge about {concept}:")
            print("\n" + challenge.code)
            
            # Get user solution
            print("\nPlease provide your improved version of the code.")
            print("Enter your solution (type 'DONE' on a new line when finished):")
            
            user_solution = []
            while True:
                line = input()
                if line == 'DONE':
                    break
                user_solution.append(line)
            
            # Evaluate solution
            print("\nEvaluating your solution...")
            evaluation = self.provider.evaluate_solution(
                challenge.code, 
                '\n'.join(user_solution)
            )
            
            # Display results
            print(f"\nScore: {evaluation.score}/100")
            print("\nImprovements made:")
            for imp in evaluation.improvements:
                print(f"✓ {imp}")
            
            if evaluation.suggestions:
                print("\nSuggestions for further improvement:")
                for sugg in evaluation.suggestions:
                    print(f"• {sugg}")
            
            print(f"\nExplanation: {evaluation.explanation}")
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")

def main():
    # Example of provider selection
    dotenv.load_dotenv()
    provider = lambda: OpenAIProvider(os.getenv('OPENAI_API_KEY'))
    
    tool = CodePracticeTool(provider())
    tool.run_practice_session()

if __name__ == "__main__":
    main()