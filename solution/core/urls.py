from django.urls import path, include
from core.settings import API_VERSION

urlpatterns = [
    path(f'api/{API_VERSION}/task', include('task.urls')),
    path(f'api/{API_VERSION}/', include('authentication.urls')),
]
