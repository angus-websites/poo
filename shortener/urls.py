from django.urls import path
from . import views

urlpatterns = [
    path('', views.shorten_url, name='shorten_url'),                            # Shorten the URL
    path('<str:short_code>/', views.redirect_url, name='redirect_url'),         # Redirect to the original URL
    path('shortened/<str:short_code>/', views.shortened_url, name='shortened')  # Display the shortened URL
]
