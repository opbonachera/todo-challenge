
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer
from .filters import TaskFilter

class TaskViewSet(viewsets.ModelViewSet):
    """
    Provides full CRUD for Task model with soft delete.
    """
    queryset = Task.objects.filter(deleted=False)
    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter]
    filterset_class = TaskFilter
    ordering_fields = ['created_at', 'priority', 'title']
    ordering = ['-created_at']
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        """GET /task/ → list all tasks (with filtering and ordering)"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """GET /task/<id>/ → get single task"""
        task = self.get_object()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """POST /task/ → create a new task"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """PUT /task/<id>/ → full update"""
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """PATCH /task/<id>/ → partial update"""
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """DELETE /task/<id>/ → soft delete"""
        task = self.get_object()
        task.deleted = True
        task.save()
        return Response({"message": f"deleted task with id {task.id}"}, status=status.HTTP_200_OK)
