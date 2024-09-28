from django.contrib import admin
from django.urls import path, include
from quality_checks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('quality_checks.urls')),  # Include app URLs
    path('', views.index),  # Root URL points to the index view
]
