from django.urls import path
from .views import EventListCreateView, EventDetailView, UpcomingEventsView

urlpatterns = [
    path('', EventListCreateView.as_view(), name='events-list-create'),
    path('<int:pk>/', EventDetailView.as_view(), name='events-detail'),
    path('upcoming/', UpcomingEventsView.as_view()),
]
