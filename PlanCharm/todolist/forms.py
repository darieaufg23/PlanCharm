from django import forms
from .models import Event, Note, CustomUser
from datetime import datetime
from django.utils import timezone

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        if start_time:
            if isinstance(start_time, str):
                try:
                    start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
                except ValueError:
                    raise forms.ValidationError('Неправильний формат часу початку. Використовуйте формат YYYY-MM-DDTHH:MM.')
            if timezone.is_naive(start_time):
                start_time = timezone.make_aware(start_time)
        return start_time

    def clean_end_time(self):
        end_time = self.cleaned_data.get('end_time')
        if end_time:
            if isinstance(end_time, str):
                try:
                    end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')
                except ValueError:
                    raise forms.ValidationError('Неправильний формат часу закінчення. Використовуйте формат YYYY-MM-DDTHH:MM.')
            if timezone.is_naive(end_time):
                end_time = timezone.make_aware(end_time)
        return end_time

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content', 'date_time']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_date_time(self):
        date_time = self.cleaned_data.get('date_time')
        if date_time:
            if isinstance(date_time, str):
                try:
                    date_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
                except ValueError:
                    raise forms.ValidationError('Неправильний формат дати та часу. Використовуйте формат YYYY-MM-DDTHH:MM.')
            if timezone.is_naive(date_time):
                date_time = timezone.make_aware(date_time)
        return date_time

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
