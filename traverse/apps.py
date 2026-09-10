from django.apps import AppConfig


class TraverseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'traverse'

    def ready(self):
        import traverse.signals   
