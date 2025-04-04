from flask import Flask, render_template, request, jsonify
from AI import create_personalized_system_prompt, handle_api_request, remove_emojis
from openai import OpenAI
import os
import time

app = Flask(__name__)

# Default user profile
default_profile = {
    "Hi there, I am your personalized tutor from TUEX. How old are you?": "15",
    "Awesome! I love to work with students your age! What are some of your favorite activities? What really amaze you?": "coding, music, and games",
    "You know what I find that super cool as well! What kind of music do you like? I like to listen to music while I work and study.": "pop and rock",
    "Do you prefer fiction or non-fiction? I like to read both!": "fiction",
    "What's your favorite subject or field of study in school? For me I really love math and science!": "computer science",
    "Are you more of a morning person or night owl? I'm a night owl, but I try to wake up early to start my day, It's important to get enough sleep.": "night owl",
    "What's your preferred way to learn (reading, watching, doing)? I like to do and watch videos, but I also like to read.": "doing",
    "What's your favorite season? I like spring and summer, but I also like winter because I can play with snow.": "summer",
    "Do you prefer indoor or outdoor activities? I like both, but I prefer outdoor activities like playing soccer and basketball.": "indoor",
    "What's your communication style (formal, casual, technical)?": "casual",
    "What's your preferred language?": "English"
}

user_profile = default_profile.copy()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/setup')
def setup():
    return render_template('setup.html', profile=user_profile)

@app.route('/save_profile', methods=['POST'])
def save_profile():
    global user_profile
    # Get form data
    for key in default_profile.keys():
        if key in request.form:
            user_profile[key] = request.form[key]
    
    return jsonify({"success": True, "message": "Profile saved successfully!"})

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.form.get('message', '')
    if not user_input:
        return jsonify({"error": "No message provided"})
    
    try:
        # Use the handle_api_request function from AI.py
        response = handle_api_request(user_input, user_profile)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)})

# Create templates directory if it doesn't exist
if not os.path.exists('templates'):
    os.makedirs('templates')

# For Vercel serverless deployment
app.debug = False

# This is only used when running locally. Vercel uses the app object directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 