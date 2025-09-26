import django_filters
from .models import Task
from django.db.models import Q

class TaskFilter(django_filters.FilterSet):
    text = django_filters.CharFilter(method='filter_text', label='Text search')

    class Meta:
        model = Task
        fields = {
            'priority': ['exact', 'gte', 'lte'],
            'title': ['icontains', 'exact', 'startswith', 'endswith'],
            'description': ['icontains', 'exact', 'startswith', 'endswith'],
            'updated_at': ['gte', 'lte'],
            'tags': ['icontains'],
            'completed': ['exact'],
            'updated_at': ['exact'],
            'created_at': ['exact', 'gte', 'lte'],
        }

    def filter_text(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(title__icontains=value) | Q(description__icontains=value)
            )
        return queryset
