"""
Management command to delete users who haven't logged in for 60 days
"""
from django.core.management.base import BaseCommand
from trivia.models import PublicKeyUser
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Delete users who have not logged in for 60 days'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=60,
            help='Number of days of inactivity before deletion (default: 60)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        days = options['days']
        dry_run = options['dry_run']
        
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Find inactive users
        inactive_users = PublicKeyUser.objects.filter(
            last_login__lt=cutoff_date
        ) | PublicKeyUser.objects.filter(
            last_login__isnull=True,
            created_at__lt=cutoff_date
        )
        
        count = inactive_users.count()
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would delete {count} inactive user(s) (not logged in for {days} days)'
                )
            )
            for user in inactive_users:
                last_login = user.last_login or 'Never'
                self.stdout.write(f'  - User {user.get_short_fingerprint()} (last login: {last_login})')
        else:
            deleted_count = inactive_users.delete()[0]
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted {deleted_count} inactive user(s) (not logged in for {days} days)'
                )
            )
