from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from app.models import Status


class Command(BaseCommand):
    help = 'Delete statuses older than 1 days'

    def handle(self, *args, **options):
        status = Status.objects.filter(created_at__lte=datetime.now() - timedelta(days=1))
        status.update(deleted=True)
        self.stdout.write('Deleted objects older than 1 days')
