from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(blank=True, max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(default=None, null=True, blank=True, db_index=True)
    deleted = models.BooleanField(default=False)
    priority = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)
    tags = models.TextField(blank=True, default="") # En un entorno real usaría una tabla ManyToMany
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks", db_index=True)
    
    def __str__(self):
        return self.title