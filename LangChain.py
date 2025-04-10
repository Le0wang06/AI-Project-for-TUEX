import os
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

llm = ChatDeepSeek(model="deepseek-chat", api_key=api_key)
response = llm.invoke("Sing a ballad of LangChain.")
print(response.content)