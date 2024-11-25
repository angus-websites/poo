from django.shortcuts import render, get_object_or_404, redirect
from django.utils.crypto import get_random_string
from .models import Message
from django.urls import reverse
from django.http import HttpResponseBadRequest

from .utils import generate_message_code


# View to create a new message
def create_message(request):
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if not content or len(content) > 1000:
            return HttpResponseBadRequest("Content is required and must be 1000 characters or less.")

        # Strip any script tags from the content
        content = content.replace('<script>', '').replace('</script>', '')

        # Generate a unique slug
        unique_slug = generate_message_code()

        # Save the message to the database
        Message.objects.create(slug=unique_slug, content=content)

        # Redirect to preview message page
        return redirect(reverse('preview_message', args=[unique_slug]))

    return render(request, 'message/create_message.html')

# View to preview a message URL and contents
def preview_message(request, slug):
    message = get_object_or_404(Message, slug=slug)
    return render(request, 'message/preview_message.html', {'message': message})

# View to display a message
def show_message(request, slug):
    message = get_object_or_404(Message, slug=slug)
    return render(request, 'message/show_message.html', {'message': message})

