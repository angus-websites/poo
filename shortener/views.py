from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import URL
from .utils import generate_short_code

def shorten_url(request):
    if request.method == 'POST':
        # Retrieve the original URL from POST data
        original_url = request.POST.get('original_url')

        # Basic validation check
        if not original_url:
            return JsonResponse({'error': 'URL is required'}, status=400)

        # Check if the URL already exists in the database
        existing_url = URL.objects.filter(original_url=original_url).first()
        if existing_url:
            # If the URL already exists, return the existing short code
            return JsonResponse({
                'original_url': existing_url.original_url,
                'short_url': request.build_absolute_uri(f'/{existing_url.short_code}')
            })

        # Generate a unique short code since the URL does not exist
        short_code = generate_short_code()
        url = URL.objects.create(original_url=original_url, short_code=short_code)

        # Return a JSON response with the original and shortened URLs
        return JsonResponse({
            'original_url': url.original_url,
            'short_url': request.build_absolute_uri(f'/{url.short_code}')
        })

    # Render the form if the request method is not POST
    return render(request, 'shortener/index.html')

def redirect_url(request, short_code):
    url = get_object_or_404(URL, short_code=short_code)
    return redirect(url.original_url)
