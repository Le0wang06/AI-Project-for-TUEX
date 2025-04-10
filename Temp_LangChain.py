import os
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain.prompts import PromptTemplate


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key=api_key,
    temperature=0.7,
    max_tokens=50,
    streaming=False  # Disable streaming to avoid the Stream object issue
)

prompt = PromptTemplate.from_template("Translate this to French: {text}")

# Use the new RunnableSequence syntax

user_input = input("Enter a text to translate: ")
chain = prompt | llm
response = chain.invoke({"text": user_input})
print(response.content)

