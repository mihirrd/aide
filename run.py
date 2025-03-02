import os
import dotenv
import json
from typing import List
from openai import OpenAI
from dataclasses import dataclass


@dataclass
class CodeChallenge:
    """Data class to store challenge details"""
    code: str
    concept: str
    language: str

@dataclass
class EvaluationResult:
    """Data class to store evaluation results"""
    score: int
    errors: List[str]
    suggestions: List[str]


class OpenAIProvider():
    def __init__(self, api_key: str, model: str = "chatgpt-4o-latest"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_challenge(self, concept: str, language: str) -> CodeChallenge:
        prompt = f"""State a coding interview problem based on the concept {concept} and its corresponding comment free, {language} code.
        It should have 2 to 3 Logical Bugs.
        Return only the problem statement and the code."""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a coding interviewer"},
                {"role": "user", "content": prompt}
            ]
        )

        return CodeChallenge(
            code=response.choices[0].message.content.strip(),
            concept=concept,
            language=language
        )

    def _create_evaluation_prompt(self, original_code: str, user_solution: str) -> str:
        """Create a standardized evaluation prompt"""
        return f"""Compare the original code and the user's solution:

        Original code:
        {original_code}

        User's solution:
        {user_solution}

        Provide an evaluation in the following JSON format:
        {{
            "score": <number between 0-100>,
            "errors": [<list all the bugs present in earlier (original) code>],
            "suggestions": [<list of potential further suggestions>],
        }}

        Base the score on:
        - 0 points if the bug is not fixed
        - 100 points if all the bugs and styling issues are fixed
        - 50 points if the bugs are fixed but the code clarity is bad.
        - 20 points if code clarity is good but the bug is not solved.

        Ensure the response is valid JSON."""

    def evaluate_solution(self, original_code: str, user_solution: str) -> EvaluationResult:
        prompt = self._create_evaluation_prompt(original_code, user_solution)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a interviewer evaluating candidate's solutions."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )

        result = json.loads(response.choices[0].message.content)
        return EvaluationResult(**result)


class CodePracticeTool:
    def __init__(self, provider: OpenAIProvider):
        self.provider = provider
        self.programming_concepts = [
            "Two pointers", "Sliding window pattern", "Arrays", "Linked Lists",
            "Binary search", "Stacks", "Queues", "Heap", "Trees", "Sorting"
        ]
        self.programming_languages =[
            "Python", "Clojure", "Java", "Javascript", "C++"
        ]

    def run_practice_session(self):
        """Run an interactive practice session"""
        print("Welcome to Code Coach AI!")

        print("\nProgramming Languages:")
        for i, language in enumerate(self.programming_languages, 1):
            print(f"{i}. {language}")

        lang_idx = int(input("\nChoose a language (enter number): ")) - 1
        language = self.programming_languages[lang_idx]

        print("\nCoding concepts:")
        for i, concept in enumerate(self.programming_concepts, 1):
            print(f"{i}. {concept}")

        concept_idx = int(input("\nChoose a programming concept (enter number): ")) - 1
        concept = self.programming_concepts[concept_idx]


        try:
            # Generate challenge
            print("\nGenerating challenge...")
            challenge = self.provider.generate_challenge(concept, language)
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
            print("\nErrors in the code:")
            for errs in evaluation.errors:
                print(f"- {errs}")

            if evaluation.suggestions:
                print("\nSuggestions for further improvement:")
                for sugg in evaluation.suggestions:
                    print(f"• {sugg}")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

def main():
    dotenv.load_dotenv()
    provider = lambda: OpenAIProvider(os.getenv('OPENAI_API_KEY'))

    tool = CodePracticeTool(provider())
    tool.run_practice_session()

if __name__ == "__main__":
    main()
