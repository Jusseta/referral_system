import random
from django.utils.crypto import get_random_string


def create_auth_code():
    """Generating random authentication code"""
    return random.randint(1000, 9999)


def create_invite_code():
    """Generating random invitation code"""
    return get_random_string(length=6)


def send_auth_code(auth_code):
    """Sending a message to terminal"""
    print(f'Your authentication code: {auth_code}')
