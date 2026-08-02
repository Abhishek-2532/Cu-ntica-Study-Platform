import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

if not MONGO_URI:
    print("\n[DATABASE ERROR] MONGO_URI is missing from your .env file.")
    sys.exit(1)

if not DATABASE_NAME:
    print("\n[DATABASE ERROR] DATABASE_NAME is missing from your .env file.")
    sys.exit(1)

# Bug #11 Fix: Test MongoDB connection at startup.
# By default, MongoClient connects lazily, so a bad URI or connection failure
# would only raise exceptions when a user hits a database route.
# We ping the admin database with a 5-second timeout to fail-fast on startup.
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # Ping the server to check connection status
    client.admin.command("ping")
    print(f"Database: Connected successfully to MongoDB database '{DATABASE_NAME}'.")
except Exception as e:
    print(
        f"\n[DATABASE CONNECTION ERROR] Could not connect to MongoDB.\n"
        f"URI: {MONGO_URI.split('@')[-1] if '@' in MONGO_URI else MONGO_URI}\n"
        f"Error: {e}\n"
        f"Please verify that:\n"
        f" 1. Your network connection is active.\n"
        f" 2. The MongoDB server/cluster is online.\n"
        f" 3. Your IP address is whitelisted in MongoDB Atlas Network Access.\n"
        f" 4. Your credentials (username/password) are correct in .env.\n"
    )
    sys.exit(1)

db = client[DATABASE_NAME]