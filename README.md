# DeepSeek API Integration

This is a simple implementation of the DeepSeek API for text generation.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your DeepSeek API key:
   - Get your API key from the DeepSeek platform
   - Set it as an environment variable:
     ```bash
     # On Windows
     set DEEPSEEK_API_KEY=your-api-key
     
     # On Unix/Linux/MacOS
     export DEEPSEEK_API_KEY=your-api-key
     ```
   - Or create a `.env` file in the project root with:
     ```
     DEEPSEEK_API_KEY=your-api-key
     ```

## Usage

Run the script:
```bash
python AI.py
```

The script includes a simple example that asks "What is artificial intelligence?" and prints the response.

## Customization

You can modify the `generate_text()` function in `AI.py` to:
- Change the model (currently set to "deepseek-chat")
- Adjust the temperature (currently 0.7)
- Modify the max_tokens (currently 1000)
- Add more parameters as needed

## Error Handling

The script includes basic error handling and will print any API-related errors that occur during execution. 