
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
        queryset = self.get_queryset().filter(created_by=request.user)        
        queryset = self.filter_queryset(queryset)

        serializer = self.get_serializer(queryset, many=True)

              
        logger.info(f'{request.user} - Listed task ids {[ data.get("id") for data in serializer.data]} with filters: {request.query_params}')
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(task)

        logger.info(f'{request.user} - Retrieved task with id: {task.id}')
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)

        logger.info(f'{request.user} - Created task with id: {serializer.data["id"]}')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data)
        
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['updated_at'] = datetime.now()
        serializer.save()

        logger.info(f'{request.user} - Updated task with id {task.id}.')
        return Response(serializer.data)
        
    def partial_update(self, request, *args, **kwargs):
        task = self.get_object()

        serializer = self.get_serializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['updated_at'] = datetime.now()
        serializer.save()

        logger.info(f'{request.user} - Partially updated task with id {task.id}.')
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.deleted = True
        task.save()
        
        logger.info(f'{request.user} - Soft deleted task with id {task.id}')
        return Response({"message": f"deleted task with id {task.id}"}, status=status.HTTP_200_OK)
    