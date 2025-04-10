import os 
from langchain.llms import OpenAI


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



def main():
  llm = OpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
  response = llm.invoke("Summarize the history of the internet in 3 sentences.")
  print(response)

if __name__ == "__main__":
    main()









