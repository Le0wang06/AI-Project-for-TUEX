from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("DEEPSEEK_API_KEY not found in environment variables")

model = ChatOpenAI(
    model="deepseek-chat",
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

def main():
    response = model.invoke("Summarize the history of the internet in 3 sentences.")
    print(response.content)

if __name__ == "__main__":
    main()
