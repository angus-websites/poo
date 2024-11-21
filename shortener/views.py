from django.shortcuts import render, redirect, get_object_or_404
from .models import URL
from .utils import generate_short_code

def shorten_url(request):
    if request.method == 'POST':
        # Retrieve the original URL from POST data
        original_url = request.POST.get('original_url')

        # Basic validation check
        if not original_url:
            return render(request, 'shortener/index.html', {'error': 'URL is required'})

        # Check if the URL already exists in the database
        existing_url = URL.objects.filter(original_url=original_url).first()
        if existing_url:
            # If the URL already exists, use the existing short code
            short_code = existing_url.short_code
        else:
            # Generate a unique short code since the URL does not exist
            short_code = generate_short_code()

            # Save the URL to the database
            URL.objects.create(original_url=original_url, short_code=short_code)

        # Redirect to the view that displays the shortened URL
        return redirect('shortened', short_code=short_code)

    # Render the form if the request method is not POST
    return render(request, 'shortener/index.html')

def shortened_url(request, short_code):
    """View to display the shortened URL."""

    # Validate the short code exists in the database
    get_object_or_404(URL, short_code=short_code)

    return render(request, 'shortener/shortened.html', {'short_url': request.build_absolute_uri(f"/{short_code}")})

def redirect_url(request, short_code):
    url = get_object_or_404(URL, short_code=short_code)
    return redirect(url.original_url)
