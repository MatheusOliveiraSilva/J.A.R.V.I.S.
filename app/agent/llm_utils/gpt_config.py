import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../../.env")

AZURE_OPENAI_BASE_URL = "https://azure-openai-danke.openai.azure.com/openai"

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_API_VERSION = '2024-02-15-preview'

MODEL_4O = 'gpt-4o'
MODEL_EMBEDDING = 'text-embedding-ada-002'