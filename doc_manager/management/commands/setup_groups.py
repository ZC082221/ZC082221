# doc_manager/management/commands/setup_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Creates predefined user groups for roles.'

    def handle(self, *args, **options):
        roles = ['View-Only', 'Employee', 'Admin', 'Approver']
        for role_name in roles:
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created group "{role_name}"'))
            else:
                self.stdout.write(f'Group "{role_name}" already exists.')
        self.stdout.write("Group creation/check complete.")
