from django.db import models

class SlackUser(models.Model):
    # SCIM Core User Schema
    scim_id = models.CharField(max_length=255, unique=True, db_index=True)
    external_id = models.CharField(max_length=255, blank=True, null=True)
    user_name = models.CharField(max_length=255, unique=True)
    
    # Name attributes
    formatted_name = models.CharField(max_length=255, blank=True)
    family_name = models.CharField(max_length=100, blank=True)
    given_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    honorific_prefix = models.CharField(max_length=50, blank=True)
    honorific_suffix = models.CharField(max_length=50, blank=True)
    
    # Contact info
    display_name = models.CharField(max_length=255, blank=True)
    nick_name = models.CharField(max_length=100, blank=True)
    profile_url = models.URLField(blank=True)
    title = models.CharField(max_length=100, blank=True)
    user_type = models.CharField(max_length=50, blank=True)
    preferred_language = models.CharField(max_length=10, blank=True)
    locale = models.CharField(max_length=10, blank=True)
    timezone = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=255, blank=True)
    
    # Status
    active = models.BooleanField(default=True)
    
    # Enterprise extension
    employee_number = models.CharField(max_length=50, blank=True)
    cost_center = models.CharField(max_length=50, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    division = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=255, blank=True)
    manager_id = models.CharField(max_length=50, blank=True)
    
    # Slack extension
    start_date = models.DateTimeField(blank=True, null=True)
    
    # Slack specific
    slack_user_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    team_id = models.CharField(max_length=50, blank=True)
    
    # Metadata
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    version = models.CharField(max_length=50, blank=True)
    location = models.URLField(blank=True)
    
    class Meta:
        db_table = 'slack_users'
        
    def __str__(self):
        return self.user_name

class SlackUserEmail(models.Model):
    user = models.ForeignKey(SlackUser, on_delete=models.CASCADE, related_name='emails')
    value = models.EmailField()
    type = models.CharField(max_length=20, default='work')
    primary = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'slack_user_emails'

class SlackUserPhoneNumber(models.Model):
    user = models.ForeignKey(SlackUser, on_delete=models.CASCADE, related_name='phone_numbers')
    value = models.CharField(max_length=20)
    type = models.CharField(max_length=20, default='work')
    primary = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'slack_user_phone_numbers'

class SlackUserAddress(models.Model):
    user = models.ForeignKey(SlackUser, on_delete=models.CASCADE, related_name='addresses')
    formatted = models.TextField(blank=True)
    street_address = models.CharField(max_length=255, blank=True)
    locality = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=20, default='work')
    primary = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'slack_user_addresses'

class SlackUserGroup(models.Model):
    user = models.ForeignKey(SlackUser, on_delete=models.CASCADE, related_name='groups')
    value = models.CharField(max_length=255)
    display = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=20, default='direct')
    
    class Meta:
        db_table = 'slack_user_groups'

class SlackUserPhoto(models.Model):
    user = models.ForeignKey(SlackUser, on_delete=models.CASCADE, related_name='photos')
    value = models.URLField()
    type = models.CharField(max_length=20, default='photo')
    
    class Meta:
        db_table = 'slack_user_photos'

class SlackUserRole(models.Model):
    user = models.ForeignKey(SlackUser, on_delete=models.CASCADE, related_name='roles')
    value = models.CharField(max_length=255)
    primary = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'slack_user_roles'