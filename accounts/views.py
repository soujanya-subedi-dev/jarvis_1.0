from rest_framework import generics, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from .serializers import (
    UserSerializer, UserRegisterSerializer, ProfileSerializer
)

# Register (public)
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


# User detail / list (admin-only for list)
class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()


# Profile (own profile)
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


# Password_change
class PasswordChangeView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.Serializer  # no fields, only body

    def update(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({"old_password": "Wrong password."}, status=400)

        try:
            validate_password(new_password, user)
        except Exception as e:
            return Response({"new_password": str(e)}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password updated."})


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def password_reset_request(request):
    email = request.data.get('email')
    if not email:
        return Response({"detail": "email required"}, status=400)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"detail": "If that email exists, a reset link has been sent."})

    token = default_token_generator.make_token(user)
    uid = user.pk

    reset_url = f"{settings.FRONTEND_URL}/password-reset/?uid={uid}&token={token}"

    send_mail(
        subject="Jarvis Password Reset",
        message=f"Reset your password: {reset_url}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )

    return Response({"detail": "If that email exists, a reset link has been sent."})


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def password_reset_confirm(request):
    uid = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('new_password')

    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return Response({"detail": "Invalid reset link"}, status=400)

    if not default_token_generator.check_token(user, token):
        return Response({"detail": "Invalid or expired token"}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({"detail": "Password has been reset."})


# Role assignment (admin only)
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def assign_role(request, user_id):
    role = request.data.get('role')

    if not role:
        return Response({"detail": "role required"}, status=400)

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response(status=404)

    group, _ = Group.objects.get_or_create(name=role)
    user.groups.add(group)

    return Response({"detail": "role assigned"})
