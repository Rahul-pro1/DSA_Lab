from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not set in environment variables.")

client = MongoClient(MONGODB_URI)
db = client["code_exec_platform"]
problems_collection = db["problems"]
