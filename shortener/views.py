from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import URL
from .utils import generate_short_code
from .forms import URLForm

def shorten_url(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            original_url = form.cleaned_data['original_url']
            short_code = generate_short_code()
            url, created = URL.objects.get_or_create(original_url=original_url, defaults={'short_code': short_code})

            return JsonResponse({
                'original_url': url.original_url,
                'short_url': request.build_absolute_uri(f'/{url.short_code}')
            })
    else:
        form = URLForm()

    return render(request, 'shortener/index.html', {'form': form})

def redirect_url(request, short_code):
    url = get_object_or_404(URL, short_code=short_code)
    return redirect(url.original_url)
