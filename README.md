# TUEX AI Tutor

A personalized AI tutoring platform that adapts to individual learning styles and preferences.

## Features

- Personalized learning experience based on user profile
- Natural voice interaction with text-to-speech
- Web interface for easy access
- Mobile-friendly responsive design

## Setup for Local Development

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the application locally:
   ```
   python app.py
   ```

3. Open your browser and go to `http://127.0.0.1:8080`

## Deploying to Vercel

Follow these steps to deploy your TUEX AI Tutor to Vercel:

1. Install the Vercel CLI:
   ```
   npm install -g vercel
   ```

2. Log in to Vercel:
   ```
   vercel login
   ```

3. Deploy your application:
   ```
   vercel
   ```

4. Follow the prompt instructions. When asked:
   - Select "Continue with default project settings"
   - Confirm your deployment

5. Once deployed, Vercel will provide you with a URL for your live application.

### Environment Variables

Make sure to set these environment variables in your Vercel project settings:
- `OPENAI_API_KEY`: Your DeepSeek AI API key

## Usage

1. Visit the deployed application URL
2. Set up your profile by answering the personalization questions
3. Start chatting with your AI tutor!

## Technologies Used

- Flask (Python web framework)
- OpenAI/DeepSeek API for AI capabilities
- gTTS for text-to-speech
- Bootstrap for responsive design 