from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'deadline']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'pl. Bevásárlás',
                'style': 'width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Részletes leírás...',
                'style': 'width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px; resize: vertical; min-height: 100px;'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px;'
            }),
            'deadline': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'style': 'width: 100%; padding: 10px; border: 2px solid #ddd; border-radius: 5px; font-size: 16px;'
            }, format='%Y-%m-%dT%H:%M'),
        }
        
        labels = {
            'title': 'Feladat neve',
            'description': 'Leírás',
            'priority': 'Prioritás',
            'status': 'Státusz',
            'deadline': 'Határidő',
        }
    
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['deadline'].required = False
        if self.instance and self.instance.deadline:
            self.initial['deadline'] = self.instance.deadline.strftime('%Y-%m-%dT%H:%M')