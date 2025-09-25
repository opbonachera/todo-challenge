from django.urls import path
from .views import TaskViewSet

task_list = TaskViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

task_detail = TaskViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [
    path('', task_list, name='task-list'),
    path('/<int:pk>', task_detail, name='task-detail'),
]
