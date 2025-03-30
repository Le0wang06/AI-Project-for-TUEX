# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
import time
import sys


client = OpenAI(api_key="sk-4c9926abc4d44e21978dfba16b35a043", base_url="https://api.deepseek.com")

def get_user_profile():
    print("\nLet's personalize your experience! Please answer these quick questions:")
    profile = {}
    
    questions = [
        "What's your age?",
        "What are your main interests or hobbies?",
        "What's your favorite type of music?",
        "Do you prefer fiction or non-fiction?",
        "What's your favorite subject or field of study?",
        "Are you more of a morning person or night owl?",
        "What's your preferred way to learn (reading, watching, doing)?",
        "What's your favorite season?",
        "Do you prefer indoor or outdoor activities?",
        "What's your communication style (formal, casual, technical)?"
    ]
    
    for question in questions:
        while True:
            answer = input(f"\n{question}\n> ").strip()
            if answer:  # Only accept non-empty answers
                profile[question] = answer
                break
            print("Please provide an answer.")
    
    return profile

def create_personalized_system_prompt(profile):
    interests = profile["What are your main interests or hobbies?"]
    communication_style = profile["What's your communication style (formal, casual, technical)?"]
    age = profile["What's your age?"]
    
    return f"""You are a personalized AI assistant for a {age}-year-old who is interested in {interests}. 
    Use a {communication_style} communication style. Be engaging and relate responses to their interests.
    Keep responses concise but friendly. If relevant, incorporate their interests in music ({profile["What's your favorite type of music?"]}),
    preferred learning style ({profile["What's your preferred way to learn (reading, watching, doing)?"]}),
    and other preferences to make responses more personal."""

def handle_api_request(user_input, profile, max_retries=3):
    for attempt in range(max_retries):
        try:
            print("\nResponse: ", end="", flush=True)
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": create_personalized_system_prompt(profile)},
                    {"role": "user", "content": user_input},
                ],
                temperature=0.7,
                max_tokens=1000,
                presence_penalty=0.6,
                frequency_penalty=0.6,
                stream=True,
                top_p=0.95,
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

def main():
    print("Welcome to your personalized AI assistant!")
    profile = get_user_profile()
    print("\nGreat! Now I know more about you. Let's start chatting!")
    
    while True:
        try:
            UserInput = input("\nEnter your question (or 'quit' to exit): ")
            if UserInput.lower() == 'quit':
                break
                
            handle_api_request(UserInput, profile)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()