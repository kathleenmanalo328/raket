import secrets
import string

ALPHABET = string.ascii_letters + string.digits

def generate_id(prefix, length=12):
    suffix = "".join(secrets.choice(ALPHABET) for _ in range(length))
    return f"{prefix}{suffix}"