from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_message, name='create_message'),
    path('show/<slug:slug>/', views.show_message, name='show_message'),
    path('preview/<slug:slug>/', views.preview_message, name='preview_message'),
]
