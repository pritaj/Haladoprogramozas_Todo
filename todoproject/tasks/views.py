from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Task
from .forms import TaskForm
from . import analytics


def task_list(request):
    """Összes feladat listázása"""
    tasks = Task.objects.all()

    # Szűrés státusz alapján
    status_filter = request.GET.get('status')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    # Szűrés prioritás alapján
    priority_filter = request.GET.get('priority')
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    # Határidő státusz hozzáadása minden feladathoz
    now = timezone.now()
    for task in tasks:
        if task.deadline and task.status != 'done':
            if task.deadline < now:
                task.deadline_status = 'overdue'
            elif task.deadline < now + timedelta(hours=24):
                task.deadline_status = 'soon'
            else:
                task.deadline_status = 'ok'
        else:
            task.deadline_status = None

    context = {
        'tasks': tasks,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
    }
    return render(request, 'tasks/task_list.html', context)


def task_create(request):
    """Új feladat létrehozása"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        deadline = request.POST.get('deadline')

        Task.objects.create(
            title=title,
            description=description,
            priority=priority,
            deadline=deadline if deadline else None
        )
        return redirect('task_list')

    return render(request, 'tasks/task_create.html')


def task_update(request, pk):
    """Feladat szerkesztése"""
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'tasks/task_update.html', {'form': form, 'task': task})


def task_delete(request, pk):
    """Feladat törlése"""
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    context = {'task': task}
    return render(request, 'tasks/task_delete.html', context)


def task_toggle(request, pk):
    """Feladat státuszának gyors váltása"""
    task = get_object_or_404(Task, pk=pk)
    if task.status == 'done':
        task.status = 'todo'
    else:
        task.status = 'done'
    task.save()
    return redirect('task_list')


def task_analytics(request):
    """Elemzések és statisztikák"""
    completion_stats = analytics.get_completion_statistics()
    priority_stats = analytics.get_priority_statistics()
    status_distribution = analytics.get_status_distribution()
    weekly_trend = analytics.get_weekly_completion_trend()
    
    predictions = {
        'low': analytics.predict_task_completion('low'),
        'medium': analytics.predict_task_completion('medium'),
        'high': analytics.predict_task_completion('high'),
    }
    
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(status='done').count()
    pending_tasks = Task.objects.filter(status__in=['todo', 'in_progress']).count()
    
    now = timezone.now()
    overdue_tasks = Task.objects.filter(
        deadline__lt=now,
        status__in=['todo', 'in_progress']
    ).count()
    
    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'completion_stats': completion_stats,
        'priority_stats': priority_stats,
        'status_distribution': status_distribution,
        'weekly_trend': weekly_trend,
        'predictions': predictions,
    }
    
    return render(request, 'tasks/task_analytics.html', context)