from django.apps import AppConfig

class SlackScimConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'slack_scim'
    verbose_name = 'Slack SCIM'
    
    def ready(self):
        import slack_scim.signals