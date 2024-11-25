from django.shortcuts import render, redirect, get_object_or_404

from poo.util import shorten
from .models import URL
from .utils import generate_short_code
from django.http import HttpRequest, HttpResponse

def shorten_url(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        # Retrieve the original URL from POST data
        original_url = request.POST.get('original_url')

        # Basic validation check
        if not original_url:
            return render(request, 'shortener/index.html', {'error': 'URL is required'})

        # Shorten the URL
        short_code = shorten(original_url)

        # Redirect to the view that displays the shortened URL
        return redirect('shortened', short_code=short_code)

    # Render the form if the request method is not POST
    return render(request, 'shortener/index.html')

def shortened_url(request: HttpRequest, short_code: str) -> HttpResponse:
    """View to display the shortened URL."""

    # Validate the short code exists in the database
    get_object_or_404(URL, short_code=short_code)

    return render(request, 'shortener/shortened.html', {'short_url': request.build_absolute_uri(f"/{short_code}")})

def redirect_url(request: HttpRequest, short_code: str) -> HttpResponse:
    url = get_object_or_404(URL, short_code=short_code)

    # Update the access information
    url.record_access()

    # Redirect to the original URL
    return redirect(url.original_url)
