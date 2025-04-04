# Please install OpenAI SDK first: `pip3 install openai`
# Also install pyttsx3: `pip install pyttsx3`

from openai import OpenAI
import time
import sys
from gtts import gTTS
import os
import pygame
import re

client = OpenAI(api_key="sk-4c9926abc4d44e21978dfba16b35a043", base_url="https://api.deepseek.com")

def remove_emojis(text):
    """Remove emojis from text"""
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
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

def speak(text):
    """Convert text to speech with natural, expressive voice"""
    # Remove emojis before converting to speech
    clean_text = remove_emojis(text)
    
    # Add natural pauses and emphasis
    sentences = clean_text.split('.')
    processed_text = ''
    for sentence in sentences:
        if sentence.strip():
            # Add slight pause after each sentence
            processed_text += sentence.strip() + '. '
            # Add longer pause after questions
            if '?' in sentence:
                processed_text += ' '
    
    # Create gTTS object with natural parameters
    tts = gTTS(
        text=processed_text,
        lang='en',
        slow=False,
        tld='com',  # Use US English accent
        lang_check=False  # Allow more natural speech
    )
    
    # Save the audio file
    tts.save("temp_speech.mp3")
    
    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Load and play the audio file
    pygame.mixer.music.load("temp_speech.mp3")
    pygame.mixer.music.play()
    
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    # Clean up the temporary file
    try:
        os.remove("temp_speech.mp3")
    except:
        pass

def get_user_profile():
    print("\nLet's personalize your experience! Please answer these quick questions:")

    # Map for question to answer

    profile = {}


    #list of questions
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

    
    for question in questions:
        while True:
            answer = input(f"\n{question}\n> ").strip()
            if answer:  # Only accept non-empty answers
                profile[question] = answer
                break
            print("Please provide an answer.")
    return profile




def create_personalized_system_prompt(profile):
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
            
            # Speak the response
            speak(full_response)
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

    #collecting user profile+ trigger the chat

    profile = get_user_profile()
    print("\nGreat! Now I know more about you. Let's start chatting!")
    
    #running the chat 
    while True:
        try:
            UserInput = input("\nEnter your question (or 'quit' to exit): ")
            if UserInput.lower() == 'quit':
                print("\nGoodbye!")
                break
            handle_api_request(UserInput, profile)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()