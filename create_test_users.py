import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_scim.settings')
django.setup()

from slack_scim.models import SlackUser

# Check existing users
print(f"Current users in database: {SlackUser.objects.count()}")
for user in SlackUser.objects.all():
    print(f"- {user.display_name} ({user.user_name})")

if SlackUser.objects.count() == 0:
    # Create test users only if none exist
    users_data = [
        {
            'user_name': 'john.doe@example.com',
            'display_name': 'John Doe',
            'given_name': 'John',
            'family_name': 'Doe',
            'active': True
        },
        {
            'user_name': 'jane.smith@example.com', 
            'display_name': 'Jane Smith',
            'given_name': 'Jane',
            'family_name': 'Smith',
            'active': True
        }
    ]

    for user_data in users_data:
        user = SlackUser.objects.create(**user_data)
        print(f"Created user: {user.display_name}")

print(f"Total users in database: {SlackUser.objects.count()}")