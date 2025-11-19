from django.contrib import admin

from .models import Task

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'status', 'deadline', 'createdat']
    list_filter = ['priority', 'status', 'createdat']
    search_fields = ['title', 'description']
