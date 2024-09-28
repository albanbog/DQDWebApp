from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.basic_check),  # This connects to the basic_check view
]
