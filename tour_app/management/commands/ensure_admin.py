import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create the configured Django administrator if it does not exist.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset-password',
            action='store_true',
            help='Reset the password of an existing configured administrator.',
        )

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', '').strip()
        password = os.environ.get('ADMIN_PASSWORD', '')

        if not username and not password:
            self.stdout.write('Administrator creation skipped: credentials are not configured.')
            return
        if not username or not password:
            raise CommandError('Set both ADMIN_USERNAME and ADMIN_PASSWORD.')

        User = get_user_model()
        user, created = User.objects.get_or_create(username=username)

        changed = False
        if created or options['reset_password']:
            user.set_password(password)
            changed = True
        if not user.is_staff:
            user.is_staff = True
            changed = True
        if not user.is_superuser:
            user.is_superuser = True
            changed = True
        if changed:
            user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f'Administrator "{username}" created.'))
        else:
            self.stdout.write(f'Administrator "{username}" already exists.')
