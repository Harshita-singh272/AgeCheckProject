import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_PASSKEY = os.getenv("ADMIN_PASSKEY")

print("ADMIN_PASSKEY =", ADMIN_PASSKEY)
ADMIN_PASSKEY = os.getenv("ADMIN_PASSKEY")
