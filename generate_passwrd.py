import string
import random

def generate_password(passwrd_len: int) -> str | bool:
    characters = string.ascii_letters + string.digits + string.punctuation
    if not isinstance(passwrd_len, int):
        return False
    else:
        passwrd = ''.join(random.choice(characters) for _ in range(passwrd_len))
        return passwrd
