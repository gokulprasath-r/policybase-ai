
from google import genai
from dotenv import load_dotenv
from database import pinecone

load_dotenv();
client = genai.Client()


def generate_embedding(text: str):
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text
    )

    return response.embeddings[0].values
