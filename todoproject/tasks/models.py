from django.db import models
from django.utils import timezone
# Create your models here.
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Alacsony'),
        ('medium', 'Közepes'),
        ('high', 'Magas')
    ]
    
    STATUS_CHOICES = [
        ('todo', 'Tennivaló'),
        ('inprogress', 'Folyamatban'),
        ('done', 'Kész'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Cím')
    description = models.TextField(blank=True, verbose_name='Leírás')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name='Prioritás')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo', verbose_name='Státusz')
    deadline = models.DateTimeField(null=True, blank=True, verbose_name='Határidő')
    createdat= models.DateTimeField(auto_now_add=True, verbose_name='Létrehozva')
    updatedat= models.DateTimeField(auto_now=True, verbose_name='Módosítva')
    
    class Meta:
        ordering = [ '-createdat' ]
        verbose_name = 'Feladat'
        verbose_name_plural = 'Feladatok'
    
    def  __str__(self):
        return self.title
    
    
     
