from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allow access if user is owner of object or is staff/admin.
    Requires view.get_object() returns object with .user attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        # support objects with user attr and with owner attr
        owner = getattr(obj, 'user', None) or getattr(obj, 'owner', None)
        if owner:
            return owner == request.user
        return False
