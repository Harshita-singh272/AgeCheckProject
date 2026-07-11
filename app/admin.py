import secrets

from app.config import ADMIN_PASSKEY

def verify(passkey: str)-> bool:

    if ADMIN_PASSKEY is None:
        return False
    
    return secrets.compare_digest(
        passkey,
        ADMIN_PASSKEY
    )