# DeepSeek Personalized AI Assistant

A personalized AI assistant using the DeepSeek API that adapts to your interests and communication style.

## Setup

1. Install the required dependencies:
```bash
pip install openai
```

2. Set up your DeepSeek API key:
   - Get your API key from the DeepSeek platform
   - Replace `<DeepSeek API Key>` in the code with your actual API key

## API Documentation

### Base Configuration
- Base URL: `https://api.deepseek.com` or `https://api.deepseek.com/v1`
- Model: `deepseek-chat` (DeepSeek-V3)
- Alternative Model: `deepseek-reasoner` (DeepSeek-R1)

### Basic API Call Example
```python
from openai import OpenAI

client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)
```

### Available Parameters
- `model`: "deepseek-chat" or "deepseek-reasoner"
- `messages`: List of message objects with role and content
- `temperature`: Controls randomness (0.0 to 1.0)
- `max_tokens`: Maximum length of response
- `stream`: Enable/disable streaming responses
- `presence_penalty`: Adjust likelihood based on presence in context
- `frequency_penalty`: Adjust likelihood based on frequency in context
- `top_p`: Nucleus sampling parameter
- `n`: Number of responses to generate

## Personalized Implementation

This implementation includes:
1. User profiling system
2. Personalized responses based on user preferences
3. Streaming responses for real-time interaction
4. Error handling and retry mechanism

### Features
- Adapts communication style to user preferences
- Incorporates user interests in responses
- Real-time streaming responses
- Comprehensive error handling
- Automatic retries for recoverable errors

### Usage
1. Run the script:
```bash
python AI.py
```

2. Answer the personalization questions
3. Start chatting with your personalized AI assistant

### Example Questions
- Age and interests
- Learning preferences
- Communication style
- Activity preferences
- Music and reading preferences

## Error Handling

The implementation handles common API errors:
- 400: Invalid request format
- 401: Authentication failures
- 402: Insufficient balance
- 422: Invalid parameters
- 429: Rate limiting
- 500: Server errors
- 503: Server overload

## Notes
- The DeepSeek API is compatible with OpenAI's API format
- The v1 in base_url is for OpenAI compatibility and doesn't relate to model version
- DeepSeek-chat model is now DeepSeek-V3
- DeepSeek-reasoner is the latest DeepSeek-R1 model 