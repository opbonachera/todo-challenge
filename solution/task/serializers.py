# serializers.py
from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        db_table = 'task'
        fields = ['id', 'title', 'completed', 'created_at', 'priority', 'description', 'updated_at']
