import string
import random
from .models import URL

def generate_short_code(length: int = 6) -> str:
    """
    Generate a random short code for the URL
    :param length:
    :return: string short code
    """
    characters = string.ascii_letters + string.digits
    while True:
        short_code = ''.join(random.choice(characters) for _ in range(length))
        if not URL.objects.filter(short_code=short_code).exists():
            return short_code
