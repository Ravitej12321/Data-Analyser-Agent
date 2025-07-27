from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os



def get_model_client():
    load_dotenv()

    api_key = os.getenv("GEMINI_KEY")
    model_client = OpenAIChatCompletionClient(

    model="gemini-2.0-flash",
    api_key=api_key

    )
    return model_client 