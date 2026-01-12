#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_scim.settings')
django.setup()

from slack_scim.models import SlackUser

# Delete all users
SlackUser.objects.all().delete()
print("All users deleted successfully")