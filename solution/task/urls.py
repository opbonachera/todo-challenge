from django.urls import path, include
from .views import TaskViewSet

urlpatterns = [
    path('task', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='task'),
]
