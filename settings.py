from dotenv import load_dotenv
import os

load_dotenv()

class API_Settings:

    API_KEY = os.getenv("GOOGLE_API_KEY")