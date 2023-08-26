import os
import json
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
HOST = os.getenv('HOST')
DB = os.getenv('DB')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
ROOT = os.getenv('ROOT')
PORT = os.getenv('PORT')

if os.path.isfile("bot/admins.json"):
    pass
else:
    with open("bot/admins.json", "w") as admin_file:
        json.dump(json.dumps({'admins':[int(ROOT)]}), admin_file)