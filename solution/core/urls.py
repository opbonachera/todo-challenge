from django.urls import path, include

urlpatterns = [
    path('', include('task.urls')),
    path('', include('authentication.urls')),# Check why naming it auth is not allowed
]
