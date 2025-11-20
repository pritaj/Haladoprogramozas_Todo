from django.db.models import Avg, Count, Q
from django.utils import timezone
from .models import Task
import statistics


def get_completion_statistics():
    """
    Befejezett feladatok statisztikáinak kiszámítása
    """
    completed_tasks = Task.objects.filter(status='done')
    
    if completed_tasks.count() == 0:
        return None
    
    # Befejezési idők gyűjtése (órákban)
    completion_times = []
    for task in completed_tasks:
        time_diff = task.updatedat - task.createdat
        hours = time_diff.total_seconds() / 3600
        completion_times.append(hours)
    
    stats = {
        'total_completed': completed_tasks.count(),
        'avg_completion_time': statistics.mean(completion_times) if completion_times else 0,
        'min_completion_time': min(completion_times) if completion_times else 0,
        'max_completion_time': max(completion_times) if completion_times else 0,
        'median_completion_time': statistics.median(completion_times) if completion_times else 0,
    }
    
    return stats


def get_priority_statistics():
    """
    Prioritás szerinti statisztikák
    """
    priority_stats = {}
    
    for priority_code, priority_name in Task.PRIORITY_CHOICES:
        tasks = Task.objects.filter(priority=priority_code, status='done')
        
        if tasks.count() > 0:
            completion_times = []
            for task in tasks:
                time_diff = task.updatedat - task.createdat
                hours = time_diff.total_seconds() / 3600
                completion_times.append(hours)
            
            priority_stats[priority_name] = {
                'count': tasks.count(),
                'avg_time': statistics.mean(completion_times),
                'min_time': min(completion_times),
                'max_time': max(completion_times),
            }
        else:
            priority_stats[priority_name] = {
                'count': 0,
                'avg_time': 0,
                'min_time': 0,
                'max_time': 0,
            }
    
    return priority_stats


def linear_regression_prediction(priority='medium'):
    """
    Egyszerű lineáris regresszió implementáció
    Előrejelzi a befejezési időt prioritás alapján
    
    Args:
        priority: 'low', 'medium', vagy 'high'
    
    Returns:
        Becsült befejezési idő órákban
    """
    # Prioritás szám értéke (x tengely)
    priority_values = {'low': 1, 'medium': 2, 'high': 3}
    
    # Befejezett feladatok gyűjtése
    completed_tasks = Task.objects.filter(status='done')
    
    if completed_tasks.count() < 2:
        # Alapértelmezett értékek, ha nincs elég adat
        default_times = {'low': 24, 'medium': 48, 'high': 72}
        return default_times.get(priority, 48)
    
    # Adatok gyűjtése: x = prioritás érték, y = befejezési idő
    x_values = []
    y_values = []
    
    for task in completed_tasks:
        x = priority_values.get(task.priority, 2)
        time_diff = task.updatedat - task.createdat
        y = time_diff.total_seconds() / 3600  # órákban
        
        x_values.append(x)
        y_values.append(y)
    
    # Lineáris regresszió számítás: y = mx + b
    n = len(x_values)
    
    # Átlagok
    x_mean = sum(x_values) / n
    y_mean = sum(y_values) / n
    
    # Meredekség (m) számítása
    numerator = sum((x_values[i] - x_mean) * (y_values[i] - y_mean) for i in range(n))
    denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))
    
    if denominator == 0:
        # Ha nincs variáció, visszaadjuk az átlagot
        return y_mean
    
    m = numerator / denominator
    
    # Y-tengely metszet (b)
    b = y_mean - m * x_mean
    
    # Előrejelzés az adott prioritásra
    x_predict = priority_values.get(priority, 2)
    predicted_time = m * x_predict + b
    
    # Ne legyen negatív
    return max(predicted_time, 0.1)


def get_status_distribution():
    """
    Feladatok eloszlása státusz szerint
    """
    total = Task.objects.count()
    
    if total == 0:
        return None
    
    distribution = {}
    for status_code, status_name in Task.STATUS_CHOICES:
        count = Task.objects.filter(status=status_code).count()
        percentage = (count / total) * 100 if total > 0 else 0
        distribution[status_name] = {
            'count': count,
            'percentage': round(percentage, 1)
        }
    
    return distribution


def get_weekly_completion_trend():
    """
    Heti befejezett feladatok trendje (utolsó 4 hét)
    """
    from datetime import timedelta
    
    now = timezone.now()
    weeks_data = []
    
    for i in range(4, 0, -1):
        week_start = now - timedelta(weeks=i)
        week_end = now - timedelta(weeks=i-1)
        
        completed = Task.objects.filter(
            status='done',
            updatedat__gte=week_start,
            updatedat__lt=week_end
        ).count()
        
        weeks_data.append({
            'week': f'{i} hete',
            'completed': completed
        })
    
    return weeks_data


def predict_task_completion(priority):
    """
    Wrapper függvény a könnyebb használathoz
    """
    predicted_hours = linear_regression_prediction(priority)
    
    return {
        'priority': priority,
        'predicted_hours': round(predicted_hours, 2),
        'predicted_days': round(predicted_hours / 24, 2),
    }