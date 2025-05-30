from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VK_API_KEY = os.getenv("VK_API_KEY")
VK_GROUP_ID = os.getenv("VK_GROUP_ID")