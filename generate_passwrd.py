import string
import random


def generate_password(passwrd_len: int) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    passwrd = ''.join(random.choice(characters) for _ in range(passwrd_len))
    return passwrd


def generate_pincode(pin_len: int) -> str:
    pin_code = ''.join([str(random.randint(0, 9)) for _ in range(pin_len)])
    return pin_code
