from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .forms import EventForm, RegistrationForm, LoginForm
from .models import Event, CustomUser
from datetime import datetime
import calendar

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Реєстрація успішна!')
            return redirect('calendar')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = CustomUser.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    auth_login(request, user)
                    return redirect('calendar')
                else:
                    form.add_error(None, 'Неправильна електронна адреса або пароль')
            except CustomUser.DoesNotExist:
                form.add_error('email', 'Користувача з такою електронною адресою не існує')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def calendar_view(request, year=None, month=None):
    if year is None:
        year = datetime.now().year
    if month is None:
        month = datetime.now().month

    cal = calendar.Calendar()
    month_days = cal.itermonthdays2(year, month)
    events = Event.objects.filter(start_time__year=year, start_time__month=month, user=request.user)

    calendar_data = []
    for day, weekday in month_days:
        if day != 0:
            day_events = events.filter(start_time__day=day)
            calendar_data.append({
                'day': day,
                'weekday': calendar.day_name[weekday],
                'events': day_events
            })

    return render(request, 'calendar.html', {'calendar_data': calendar_data, 'year': year, 'month': month})

@login_required
def event_new(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            messages.success(request, 'Подія додана успішно!')
            return redirect('calendar')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})

@login_required
def event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Подія оновлена успішно!')
            return redirect('calendar')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form})

@login_required
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Подія видалена')
        return redirect('calendar')
    return render(request, 'event_confirm_delete.html', {'event': event})

def logout_view(request):
    logout(request)
    return JsonResponse({'status': 'success'}, status=200)
