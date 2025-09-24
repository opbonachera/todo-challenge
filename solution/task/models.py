from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, max_length=255)
    completed = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)
    deleted = models.BooleanField(default=False)
    priority = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=1)

    def __str__(self):
        return self.title