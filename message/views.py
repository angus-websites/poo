from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
import markdown
from shortener.models import URL
from shortener.utils import generate_short_code
from .models import Message
from django.urls import reverse
from django.http import HttpResponseBadRequest

from .utils import generate_message_code


# View to create a new message
def create_message(request):
    if request.method == 'POST':

        content = request.POST.get('content')

        if len(content) > 5000:
            messages.error(request, 'Message is too long. Please keep it under 5000 characters.')
            # Render the form
            return render(request, 'message/create_message.html', {'content': content})
        elif not content:
            messages.error(request, 'Message cannot be empty.')
            # Redirect with error message
            return redirect('create_message')

        # Strip any script tags from the content
        content = content.replace('<script>', '').replace('</script>', '')

        # Generate a unique slug
        unique_slug = generate_message_code()

        # Save the message to the database
        Message.objects.create(slug=unique_slug, content=content)

        # Create the new url
        new_url = request.build_absolute_uri(reverse('show_message', args=[unique_slug]))

        # ----- Shorten the url -----

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

            # Redirect to the view that displays the shortened URL
            return redirect('shortened', short_code=short_code)

    return render(request, 'message/create_message.html')


# View to display a message
def show_message(request, slug):
    message = get_object_or_404(Message, slug=slug)

    # Convert Markdown content to HTML
    markdown_content = markdown.markdown(
        message.content,
        extensions=[
            'markdown.extensions.extra',     # Support tables, code blocks, etc.
            'markdown.extensions.codehilite', # Code highlighting (if needed)
        ]
    )

    return render(request, 'message/show_message.html', {'message': markdown_content})

