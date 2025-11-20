from django.test import TestCase

# Create your tests here.
from tasks.models import Task
from django.utils import timezone
from datetime import timedelta


Task.objects.create(
    title='Teszt feladat',
    priority='high',
    status='done',
    createdat=timezone.now() - timedelta(days=2),
    updatedat=timezone.now() - timedelta(days=1)
)