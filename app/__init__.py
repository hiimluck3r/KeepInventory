import os
import sys
import json
from dotenv import load_dotenv
import asyncio

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
HOST = os.getenv('HOST')
DB = os.getenv('DB')
DBUSER = os.getenv('DBUSER')
PASSWORD = os.getenv('PASSWORD')
ROOT = int(os.getenv('ROOT'))
PORT = os.getenv('PORT')
loop = asyncio.get_event_loop()

print(DBUSER, DB, HOST, PORT, PASSWORD, file=sys.stderr)

with open("app/greet_user.txt") as user_greeting:
    greet_user_text = user_greeting.read()

with open("app/greet_stranger.txt") as stranger_greeting:
    greet_stranger_text = stranger_greeting.read()