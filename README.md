# AIde: AI-Powered Code Practice Tool

An intelligent coding practice tool that leverages OpenAI to generate coding challenges, evaluate solutions, and provide detailed feedback. It helps developers improve their coding skills through interactive practice sessions with AI-generated exercises.

## Features

- 🎯 Customizable difficulty levels
- 💻 Various programming concepts
- 📊 Detailed feedback and scoring
- 🔄 Interactive practice sessions
- 🎓 Educational feedback with specific improvements

## Installation

1. Clone the repository:
```bash
git clone https://github.com/mihirrd/code-coach-ai.git
cd code-coach-ai
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip3 install -r requirements.txt
```

## Configuration
1. Create .env file
2. Set up your API keys as environment variables:

### Linux/Mac:
```bash
export OPENAI_API_KEY='your-openai-key'
```

### Windows:
```bash
set OPENAI_API_KEY=your-openai-key
```

## Usage

1. Run the tool:
```bash
python run.py
```

2. Choose a programming concept and difficulty level from the available options.

3. Review the generated code challenge and implement your solution.

4. Type 'DONE' on a new line when finished with your solution.

5. Review your feedback and score.

## Available Programming Concepts

- List comprehension
- Error handling
- File handling
- Class implementation
- Data processing
- Sorting algorithm
- Recursive function
- Decorator implementation
- API interaction
- Database operations

## Difficulty Levels

- Beginner
- Intermediate
- Advanced

## Example Session

```

Available concepts:
1. list comprehension
2. error handling
3. file handling
...

Choose a concept (enter number): 1

Difficulty levels:
1. beginner
2. intermediate
3. advanced

Choose difficulty (enter number): 1

[Generated code challenge appears]

Please provide your improved version of the code.
Enter your solution (type 'DONE' on a new line when finished):
...
```

## Extending Code Coach

### Adding New Programming Concepts

Add new concepts to the `programming_concepts` list in the `CodePracticeTool` class:
```python
self.programming_concepts = [
    "existing_concept",
    "new_concept_1",
    "new_concept_2"
]
```

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Ensure environment variables are set correctly
   - Verify API keys are valid and have necessary permissions

2. **JSON Parsing Errors**
   - The tool includes fallback JSON extraction
   - Check if your selected LLM provider is returning valid JSON

3. **Network Issues**
   - Verify internet connection
   - Check if the LLM provider's service is available

### Getting Help

If you encounter issues:
1. Check the error message for specific details
2. Verify your configuration
3. Check the provider's API documentation
4. Report issues on the project's GitHub page

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
