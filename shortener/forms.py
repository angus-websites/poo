from django import forms

class URLForm(forms.Form):
    original_url = forms.URLField(
        label='Enter URL to shorten',
        widget=forms.URLInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-600',
            'placeholder': 'https://example.com'
        })
    )
