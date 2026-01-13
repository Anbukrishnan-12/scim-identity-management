#!/usr/bin/env python
import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_scim.settings')
django.setup()

from slack_scim.models import SlackUser, SlackUserEmail

def create_sample_users():
    """Create sample users for Railway deployment"""
    
    # Sample users data
    users_data = [
        {
            'user_name': 'admin@company.com',
            'display_name': 'System Administrator',
            'given_name': 'Admin',
            'family_name': 'User',
            'title': 'System Administrator',
            'active': True,
            'email': 'admin@company.com'
        },
        {
            'user_name': 'john.doe@company.com',
            'display_name': 'John Doe',
            'given_name': 'John',
            'family_name': 'Doe',
            'title': 'Software Engineer',
            'active': True,
            'email': 'john.doe@company.com'
        },
        {
            'user_name': 'jane.smith@company.com',
            'display_name': 'Jane Smith',
            'given_name': 'Jane',
            'family_name': 'Smith',
            'title': 'Product Manager',
            'active': True,
            'email': 'jane.smith@company.com'
        },
        {
            'user_name': 'mike.wilson@company.com',
            'display_name': 'Mike Wilson',
            'given_name': 'Mike',
            'family_name': 'Wilson',
            'title': 'DevOps Engineer',
            'active': True,
            'email': 'mike.wilson@company.com'
        },
        {
            'user_name': 'sarah.johnson@company.com',
            'display_name': 'Sarah Johnson',
            'given_name': 'Sarah',
            'family_name': 'Johnson',
            'title': 'UX Designer',
            'active': True,
            'email': 'sarah.johnson@company.com'
        }
    ]
    
    created_count = 0
    
    for user_data in users_data:
        # Check if user already exists
        if not SlackUser.objects.filter(user_name=user_data['user_name']).exists():
            # Create user
            user = SlackUser.objects.create(
                user_name=user_data['user_name'],
                display_name=user_data['display_name'],
                given_name=user_data['given_name'],
                family_name=user_data['family_name'],
                formatted_name=f"{user_data['given_name']} {user_data['family_name']}",
                title=user_data['title'],
                active=user_data['active'],
                employee_number=f"EMP{1000 + created_count + 1}",
                department="Engineering" if "Engineer" in user_data['title'] else "General",
                organization="SCIM Company"
            )
            
            # Create email
            SlackUserEmail.objects.create(
                user=user,
                value=user_data['email'],
                type='work',
                primary=True
            )
            
            created_count += 1
            print(f"✅ Created user: {user_data['display_name']} ({user_data['user_name']})")
        else:
            print(f"⚠️  User already exists: {user_data['user_name']}")
    
    print(f"\n🎉 Sample data creation complete! Created {created_count} new users.")
    print(f"📊 Total users in database: {SlackUser.objects.count()}")

if __name__ == '__main__':
    create_sample_users()