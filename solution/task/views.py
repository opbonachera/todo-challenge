
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import filters as drf_filters
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime

from .models import Task
from .serializers import TaskSerializer
from .filters import TaskFilter
from core.logger import logger

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(deleted=False)
    filter_backends = [DjangoFilterBackend, drf_filters.OrderingFilter]
    filterset_class = TaskFilter
    ordering_fields = ['created_at', 'priority', 'title']
    ordering = ['-created_at']
    serializer_class = TaskSerializer
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            logger.info(f'Listed {len(serializer.data)} task(s) with filters: {request.query_params}')
            return Response(serializer.data)
        except Exception as e:
            logger.exception(f"Error in listing tasks: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            task = self.get_object()
            serializer = self.get_serializer(task)
            logger.info(f'Retrieved task with id {task.id}')
            return Response(serializer.data)
        except Exception as e:
            logger.exception(f"Error in retrieving task: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            logger.info(f'Created task with id {serializer.data.get("id")}')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(f"Error in creating task: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            task = self.get_object()
            serializer = self.get_serializer(task, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer["data"].get("updated_at") = datetime.now()
            serializer.save()
            logger.info(f'Updated task with id {task.id}')
            return Response(serializer.data)
        except Exception as e:
            logger.exception(f"Error in updating task: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        try:
            task = self.get_object()
            serializer = self.get_serializer(task, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logger.info(f'Partially updated task with id {task.id}')
            return Response(serializer.data)
        except Exception as e:
            logger.exception(f"Error in partial update of task: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            task = self.get_object()
            task.deleted = True
            task.save()
            logger.info(f'Soft deleted task with id {task.id}')
            return Response({"message": f"deleted task with id {task.id}"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(f"Error in deleting task: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
