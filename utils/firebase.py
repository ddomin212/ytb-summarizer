import pyrebase
import os
import json
from dotenv import load_dotenv

load_dotenv()

cfg = os.getenv("FIREBASE_JSON")

firebase = pyrebase.initialize_app(json.loads(cfg))
auth = firebase.auth()
db = firebase.database()