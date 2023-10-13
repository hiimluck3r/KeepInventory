import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
HOST = os.getenv('HOST')
DB = os.getenv('DB')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
ROOT = int(os.getenv('ROOT'))
PORT = os.getenv('PORT')

with open("app/greet_user.txt") as user_greeting:
    greet_user_text = user_greeting.read()

with open("app/greet_stranger.txt") as stranger_greeting:
    greet_stranger_text = stranger_greeting.read()