import random
import string

from .models import Message


def generate_message_code(initial_length: int = 6, max_length: int = 10) -> str:
    """
    Generate a random code for message slug. Automatically increases length if no unique code is found.
    :param initial_length: Starting length for the short code.
    :param max_length: Maximum length the short code can grow to.
    :return: A unique short code as a string.
    """
    characters = string.ascii_letters + string.digits
    length = initial_length

    while length <= max_length:
        # Attempt to generate a unique short code
        for _ in range(100):  # Try 100 times before increasing the length
            code = ''.join(random.choice(characters) for _ in range(length))
            if not Message.objects.filter(short_code=code).exists():
                return code

        # If no unique code is found after 100 attempts, increase the length
        length += 1

    # If all lengths are exhausted, raise an error
    raise ValueError("Unable to generate a unique code; database may be full.")
