from django.urls import path
from .views import ( RegisterView, UserListView, UserDetailView, ProfileView, assign_role, 
                    PasswordChangeView,password_reset_request,password_reset_confirm)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),

    path('users/', UserListView.as_view()),
    path('users/<int:pk>/', UserDetailView.as_view()),
    path('users/<int:user_id>/assign-role/', assign_role),

    path('password/change/', PasswordChangeView.as_view()),
    path('password/reset/', password_reset_request),
    path('password/reset/confirm/', password_reset_confirm),
]

