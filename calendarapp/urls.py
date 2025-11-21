from django.urls import path
from .views import TodayCalendarView, WeekCalendarView, MonthCalendarView, AgendaView

urlpatterns = [
    path('today/', TodayCalendarView.as_view(), name='calendar-today'),
    path('week/', WeekCalendarView.as_view(), name='calendar-week'),
    path('month/', MonthCalendarView.as_view(), name='calendar-month'),
    path('agenda/', AgendaView.as_view(), name='calendar-agenda'),
]
