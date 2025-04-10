"""
TUEX AI Tutor - A personalized AI tutoring system
This module provides an interactive AI tutor that can engage in personalized conversations
and provide text-to-speech responses.
Bring Next Generation AI to Education with TUEX that actually care about the students. 
Contains emotional intelligence and a friendly tone.
"""

# Standard library imports
import os
import re
import sys
import time

# Third-party imports
from openai import OpenAI
from gtts import gTTS
import pygame

#This is used to get the API key from the environment variable which is private. You don't need this if you want to use the API key directly. 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration / setup API SKEY
API_KEY = os.environ.get("OPENAI_API_KEY", "ur api")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY, base_url=DEEPSEEK_BASE_URL)

def remove_emojis(text: str) -> str:
    """
    Remove emojis and special Unicode characters from text.
    
    Args:
        text (str): Input text containing emojis
        
    Returns:
        str: Clean text without emojis
    """
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

def clean_special_chars(text: str) -> str:
    """
    Remove special characters from text that might interfere with text-to-speech.
    
    Args:
        text (str): Input text containing special characters
        
    Returns:
        str: Clean text without special characters
    """
    special_chars = ['*', '_', '~', '`', '>', '<', '|', '\\', '/']
    for char in special_chars:
        text = text.replace(char, '')
    return text

def process_text_for_speech(text: str) -> str:
    """
    Process text to make it more natural for speech synthesis.
    
    Args:
        text (str): Input text to process
        
    Returns:
        str: Processed text with natural pauses
    """
    
    sentences = text.split('.')
    processed_text = ''
    for sentence in sentences:
        if sentence.strip():
            processed_text += sentence.strip() + '. '
            if '?' in sentence:
                processed_text += ' '
    return processed_text

def speak(text: str) -> None:
    """
    Convert text to speech and play it using gTTS and pygame.
    
    Args:
        text (str): Text to convert to speech
    """
    # Clean and process text
    clean_text = remove_emojis(text)
    clean_text = clean_special_chars(clean_text)
    processed_text = process_text_for_speech(clean_text)
    
    # Initialize pygame mixer if needed
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    
    # Stop any currently playing audio
    pygame.mixer.music.stop()
    time.sleep(0.1)
    
    # Generate unique filename
    temp_file = f"temp_speech_{int(time.time())}.mp3"
    
    try:
        # Create and save speech
        tts = gTTS(
            text=processed_text,
            lang='en',
            slow=False,
            tld='com',
            lang_check=False
        )
        tts.save(temp_file)
        
        # Play audio
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        
        # Wait for audio to finish
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
    except Exception as e:
        print(f"Error playing audio: {str(e)}")
    finally:
        # Clean up temporary file
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except:
            pass

def get_user_profile() -> dict:
    """
    Collect user profile information through interactive questions.
    
    Returns:
        dict: Dictionary containing user's profile information
    """
    print("\nLet's personalize your experience! Please answer these quick questions:")
    
    questions = [
        "Hi there, I am your personalized tutor from TUEX. How old are you?",
        "Awesome! I love to work with students your age! What are some of your favorite activities? What really amaze you?",
        "You know what I find that super cool as well! What kind of music do you like? I like to listen to music while I work and study.",
        "Do you prefer fiction or non-fiction? I like to read both!",
        "What's your favorite subject or field of study in school? For me I really love math and science!",
        "Are you more of a morning person or night owl? I'm a night owl, but I try to wake up early to start my day, It's important to get enough sleep.",
        "What's your preferred way to learn (reading, watching, doing)? I like to do and watch videos, but I also like to read.",
        "What's your favorite season? I like spring and summer, but I also like winter because I can play with snow.",
        "Do you prefer indoor or outdoor activities? I like both, but I prefer outdoor activities like playing soccer and basketball.",
        "What's your communication style (formal, casual, technical)?",
        "What's your preferred language?"
    ]
    
    profile = {}
    for question in questions:
        while True:
            answer = input(f"\n{question}\n> ").strip()
            if answer:
                profile[question] = answer
                break
            print("Please provide an answer.")
    return profile

def create_personalized_system_prompt(profile: dict) -> str:
    """
    Create a personalized system prompt based on user profile.
    
    Args:
        profile (dict): User's profile information
        
    Returns:
        str: Personalized system prompt for the AI
    """
    interests = profile["Awesome! I love to work with students your age! What are some of your favorite activities? What really amaze you?"]
    communication_style = profile["What's your communication style (formal, casual, technical)?"]
    age = profile["Hi there, I am your personalized tutor from TUEX. How old are you?"]
    language = profile["What's your preferred language?"]
    music = profile["You know what I find that super cool as well! What kind of music do you like? I like to listen to music while I work and study."]
    learning_style = profile["What's your preferred way to learn (reading, watching, doing)? I like to do and watch videos, but I also like to read."]
    
    return f"""You are a personalized AI tutor for TUEX Education, a Canadian tutoring platform that connects students with high-quality academic support. Your role is to help students understand and master subjects like Math, Science, and English, following Canadian curriculum standards.

Your tone is friendly, professional, patient, and encouraging. You support personalized learning by adjusting your teaching style based on the student's needs, learning pace, and background. Many of your students are multilingual, especially English-language learners from Chinese-speaking families.

You are a personalized AI assistant for a {age}-year-old who is interested in {interests}. 
Use a {communication_style} communication style. Be engaging and relate responses to their interests.
Keep responses concise but friendly. If relevant, incorporate their interests in music ({music}),
preferred learning style ({learning_style}),
and other preferences to make responses more personal.
This person speaks {language}."""

def handle_api_request(user_input: str, profile: dict, max_retries: int = 3, speak_response: bool = False) -> str:
    """
    Handle API requests to the AI model with retry logic.
    
    Args:
        user_input (str): User's input message
        profile (dict): User's profile information
        max_retries (int): Maximum number of retry attempts
        speak_response (bool): Whether to speak the response
        
    Returns:
        str: AI's response
    """
    for attempt in range(max_retries):
        try:
            if not speak_response:
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
                    if not speak_response:
                        print(content, end="", flush=True)
                    full_response += content
                    
            if not speak_response:
                print()
            
            if speak_response:
                speak(full_response)
                
            return full_response
            
        except Exception as e:
            error_str = str(e).lower()
            error_messages = {
                "400": "Invalid request format. Please check your input.",
                "401": "Authentication failed. Please check your API key.",
                "402": "Insufficient balance. Please add funds to your account.",
                "422": "Invalid parameters. Please check your request parameters.",
                "429": f"Rate limit reached. Waiting {(attempt + 1) * 2} seconds...",
                "500": "Server error. Please try again later.",
                "503": f"Server overloaded. Waiting {(attempt + 1) * 2} seconds..."
            }
            
            for code, message in error_messages.items():
                if code in error_str:
                    print(f"Error {code}: {message}")
                    if code in ["429", "503"]:
                        time.sleep((attempt + 1) * 2)
                    break
            else:
                print(f"An unexpected error occurred: {str(e)}")
            
            if attempt < max_retries - 1:
                print(f"Retrying... (Attempt {attempt + 2}/{max_retries})")
            else:
                return "Failed to get a response after multiple attempts. Please try again later."

def main() -> None:
    """Run the AI tutor in interactive mode."""
    try:
        profile = get_user_profile()
        print("\nGreat! Now I know more about you. Let's start chatting!")
        
        while True:
            try:
                user_input = input("\nEnter your question (or 'quit' to exit): ")
                if user_input.lower() == 'quit':
                    print("\nGoodbye!")
                    break
                handle_api_request(user_input, profile, speak_response=True)
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"\nAn unexpected error occurred: {str(e)}")
                
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()  
