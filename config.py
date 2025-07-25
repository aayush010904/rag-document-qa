import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX")
HACKRX_TOKEN = "b689cc51239dbe57b19d7432235ab5fd0adc0ab7bd705f4cb51920ec4c53ce9e"