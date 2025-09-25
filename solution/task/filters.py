import django_filters
from .models import Task
from django.db.models import Q

class TaskFilter(django_filters.FilterSet):
    text = django_filters.CharFilter(method='filter_text', label='Text search')
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', label='Created from')
    date_to = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', label='Created to')
    created_by = django_filters.CharFilter(field_name='created_by__username', lookup_expr='exact')
    completed = django_filters.BooleanFilter(field_name='completed', lookup_expr='exact')
    class Meta:
        model = Task
        fields = {
            'priority': ['exact', 'gte', 'lte'],
            'title': ['icontains', 'exact', 'startswith', 'endswith'],
            'description': ['icontains', 'exact', 'startswith', 'endswith'],
            'created_at': ['gte', 'lte'],
            'updated_at': ['gte', 'lte'],
        }

    def filter_text(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(title__icontains=value) | Q(description__icontains=value)
            )
        return queryset