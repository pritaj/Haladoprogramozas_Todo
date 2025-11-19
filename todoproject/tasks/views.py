from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Task

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
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.priority = request.POST.get('priority')
        task.status = request.POST.get('status')
        deadline = request.POST.get('deadline')
        task.deadline = deadline if deadline else None
        task.save()
        return redirect('task_list')

    context = {'task': task}
    return render(request, 'tasks/task_update.html', context)

def task_delete(request, pk):
    """Feladat törlése"""
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')

    context = {'task': task}
    return render(request, 'tasks/task_delete.html', context)

def task_toggle(request, pk):
    """Feladat státuszának gyors váltása (kész/folyamatban)"""
    task = get_object_or_404(Task, pk=pk)
    if task.status == 'done':
        task.status = 'todo'
    else:
        task.status = 'done'
    task.save()
    return redirect('task_list')