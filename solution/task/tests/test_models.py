# your_app/tests/test_models.py
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from ..models import Task


User = get_user_model()


class TaskModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", email="t@example.com", password="password")

    def test_create_valid_task_and_defaults(self):
        t = Task.objects.create(title="My task", created_by=self.user)
        self.assertEqual(t.title, "My task")
        self.assertFalse(t.completed, "completed should default to False")
        self.assertFalse(t.deleted, "deleted should default to False")
        self.assertEqual(t.priority, 1, "priority default should be 1")
        self.assertEqual(t.tags, "", "tags default should be an empty string")
        self.assertIsNone(t.updated_at, "updated_at default is None")

        now = timezone.now()
        delta_secs = abs((t.created_at - now).total_seconds())
        self.assertLess(delta_secs, 5, "created_at should be set to current time on save")

    def test___str__returns_title(self):
        t = Task.objects.create(title="Hello title", created_by=self.user)
        self.assertEqual(str(t), "Hello title")

    def test_title_required_and_max_length(self):

        t_empty = Task(title="", created_by=self.user)
        with self.assertRaises(ValidationError):
            t_empty.full_clean() # title must be non-empty

        t_long = Task(title="a" * 256, created_by=self.user)
        with self.assertRaises(ValidationError): 
            t_long.full_clean()

    def test_description_max_length(self):
        t_long = Task(title="long description", description="a" * 261, created_by=self.user)
        with self.assertRaises(ValidationError): 
            t_long.full_clean()


    def test_priority_validators(self):
        # priority must be between 1 and 5
        t_low = Task(title="low", priority=0, created_by=self.user)
        with self.assertRaises(ValidationError):
            t_low.full_clean()

        t_high = Task(title="high", priority=6, created_by=self.user)
        with self.assertRaises(ValidationError): # priority over 5
            t_high.full_clean()

        t_min = Task.objects.create(title="min", priority=1, created_by=self.user)
        self.assertEqual(t_min.priority, 1)
        t_max = Task.objects.create(title="max", priority=5, created_by=self.user)
        self.assertEqual(t_max.priority, 5)

    def test_tags_accepts_string(self):
        t1 = Task.objects.create(title="dict-tags", created_by=self.user, tags="a,tag")
        self.assertEqual(t1.tags, "a,tag")

    def test_created_by_fk_constraint_and_default_0_behavior(self):
        # creating a Task without a user
        t = Task(title="no-user-provided")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                t.save()

    def test_cascade_delete_user_deletes_tasks(self):
        """on_delete=models.CASCADE -> deleting the user should delete their tasks."""
        t = Task.objects.create(title="to-be-deleted", created_by=self.user)
        self.user.delete()
        self.assertFalse(Task.objects.filter(pk=t.pk).exists())


    def test_set_and_persist_updated_at(self):
        now = timezone.now()
        t = Task.objects.create(title="with-updated-at", created_by=self.user, updated_at=now)
        self.assertEqual(t.updated_at.replace(microsecond=0), now.replace(microsecond=0))

    def test_filter_by_priority(self):
        Task.objects.create(title="low", priority=1, created_by=self.user)
        Task.objects.create(title="medium", priority=3, created_by=self.user)
        Task.objects.create(title="high", priority=5, created_by=self.user)

        high_priority_tasks = Task.objects.filter(priority__gte=4)
        self.assertEqual(high_priority_tasks.count(), 1)
        self.assertEqual(high_priority_tasks.first().title, "high")

    def test_ordering_by_created_at(self):
        t1 = Task.objects.create(title="first", created_by=self.user)
        t2 = Task.objects.create(title="second", created_by=self.user)
        t3 = Task.objects.create(title="third", created_by=self.user)

        tasks = Task.objects.all().order_by('created_at')
        self.assertEqual(list(tasks), [t1, t2, t3])