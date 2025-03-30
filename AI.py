# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
import time
import sys


client = OpenAI(api_key="sk-4c9926abc4d44e21978dfba16b35a043", base_url="https://api.deepseek.com")

def handle_api_request(user_input, max_retries=3):
    for attempt in range(max_retries):
        try:
            print("\nResponse: ", end="", flush=True)
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "Be concise but informative. Use bullet points for multiple ideas."},
                    {"role": "user", "content": user_input},
                ],
                temperature=0.0,
                max_tokens=200,  # Increased for more content
                presence_penalty=0,
                frequency_penalty=0,
                stream=True,
                top_p=0.1,
                n=1
            )
            
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content
            print()  # New line after response
            return full_response
            
        except Exception as e:
            error_str = str(e).lower()
            
            if "400" in error_str:
                print("Error 400: Invalid request format. Please check your input.")
            elif "401" in error_str:
                print("Error 401: Authentication failed. Please check your API key.")
            elif "402" in error_str:
                print("Error 402: Insufficient balance. Please add funds to your account.")
            elif "422" in error_str:
                print("Error 422: Invalid parameters. Please check your request parameters.")
            elif "429" in error_str:
                wait_time = (attempt + 1) * 2
                print(f"Error 429: Rate limit reached. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            elif "500" in error_str:
                print("Error 500: Server error. Please try again later.")
                time.sleep(2)
            elif "503" in error_str:
                wait_time = (attempt + 1) * 2
                print(f"Error 503: Server overloaded. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"An unexpected error occurred: {str(e)}")
            
            if attempt < max_retries - 1:
                print(f"Retrying... (Attempt {attempt + 2}/{max_retries})")
            else:
                return "Failed to get a response after multiple attempts. Please try again later."

while True:
    try:
        UserInput = input("\nEnter your question (or 'quit' to exit): ")
        if UserInput.lower() == 'quit':
            break
            
        handle_api_request(UserInput)
        
    except KeyboardInterrupt:
        print("\nGoodbye!")
        break
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")