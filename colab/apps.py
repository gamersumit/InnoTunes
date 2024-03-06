from django.apps import AppConfig


class ColabConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'colab'

    def ready(self):
        import colab.signals