from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_message, name='create_message'),
    path('<slug:slug>/', views.show_message, name='show_message'),
]
