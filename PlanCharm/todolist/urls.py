from django.urls import path
from .views import home, register, login, calendar_view, event_new, event_edit, event_delete, logout_view

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('calendar/', calendar_view, name='calendar'),
    path('calendar/<int:year>/<int:month>/', calendar_view, name='calendar'),
    path('event/new/', event_new, name='event_new'),
    path('event/edit/<int:event_id>/', event_edit, name='event_edit'),
    path('event/delete/<int:event_id>/', event_delete, name='event_delete'),
]
