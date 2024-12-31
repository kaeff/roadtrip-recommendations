import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from a .env file if present

openapi_key = os.getenv("OPENAPI_KEY")

if openapi_key is None:
    raise ValueError("No OPENAPI_KEY found in environment variables")