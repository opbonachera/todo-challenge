# store.py
from .models import Task
from django.core.exceptions import ObjectDoesNotExist

class TaskStore:
    def add_task(self, title, description=""):
        task = Task.objects.create(title=title, description=description)
        return task

    def get_tasks(self):
        return Task.objects.filter(removed=False)

    def get_task(self, task_id):
        try:
            return Task.objects.get(id=task_id, removed=False)
        except ObjectDoesNotExist:
            return None

    def update_task(self, task_id, data):
        task = self.get_task(task_id)
        if task:
            for key, value in data.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            task.save()
        return task

    def delete_task(self, task_id):
        task = self.get_task(task_id)
        if task:
            task.removed = True
            task.save()
        return task

task_store = TaskStore()