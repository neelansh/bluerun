import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username="bluerun_admin").exists():
            User.objects.create_superuser("bluerun_admin", "bluerunfinancial@gmail.com", "bluerunfinancial2016")

