from django.apps import AppConfig


class RealitionshipConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'realitionship'
    def ready(self):
        import signals
