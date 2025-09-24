from django.urls import path, include

API_VERSION = 'v1'

urlpatterns = [
    path(f'api/{API_VERSION}/', include('task.urls')),
    path(f'api/{API_VERSION}/auth/', include('authentication.urls')),
]
