from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot, name="chatbot"),
    path('chatbot1', views.chatbot1, name="chatbot1"),


]
