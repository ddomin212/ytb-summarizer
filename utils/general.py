import os

if os.getenv("MODE") != "prod":
    from dotenv import load_dotenv

    load_dotenv()