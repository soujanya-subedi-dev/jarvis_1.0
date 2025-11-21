# accounts/management/commands/create_roles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from contacts.models import Contact

class Command(BaseCommand):
    help = "Create default roles"

    def handle(self, *args, **options):
        user_group, _ = Group.objects.get_or_create(name='user')
        manager_group, _ = Group.objects.get_or_create(name='manager')
        admin_group, _ = Group.objects.get_or_create(name='admin')

        # Example: give manager permission to change contacts
        ct = ContentType.objects.get_for_model(Contact)
        perm_change_contact = Permission.objects.get(content_type=ct, codename='change_contact')
        manager_group.permissions.add(perm_change_contact)
        print("Roles created")
