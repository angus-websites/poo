import string
import random
from .models import URL

def generate_short_code(initial_length: int = 6, max_length: int = 10) -> str:
    """
    Generate a random short code for the URL. Automatically increases length if no unique code is found.
    :param initial_length: Starting length for the short code.
    :param max_length: Maximum length the short code can grow to.
    :return: A unique short code as a string.
    """
    characters = string.ascii_letters + string.digits
    length = initial_length

    while length <= max_length:
        # Attempt to generate a unique short code
        for _ in range(100):  # Try 100 times before increasing the length
            short_code = ''.join(random.choice(characters) for _ in range(length))
            if not URL.objects.filter(short_code=short_code).exists():
                return short_code

        # If no unique code is found after 100 attempts, increase the length
        length += 1

    # If all lengths are exhausted, raise an error
    raise ValueError("Unable to generate a unique short code; database may be full.")
