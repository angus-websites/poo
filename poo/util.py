from shortener.models import URL
from shortener.utils import generate_short_code


# Shared utility functions for the poo package

def shorten(new_url: str) -> str:
    """
    Takes a URL and returns a shortened version of it.
    """

    # Check if the URL already exists in the database
    existing_url = URL.objects.filter(original_url=new_url).first()
    if existing_url:
        # If the URL already exists, use the existing short code
        short_code = existing_url.short_code
    else:
        # Generate a unique short code since the URL does not exist
        short_code = generate_short_code()

        # Save the URL to the database
        URL.objects.create(original_url=new_url, short_code=short_code)

    return short_code
