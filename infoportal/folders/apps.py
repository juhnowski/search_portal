from django.apps import AppConfig


class FoldersConfig(AppConfig):
    name = 'folders'
    verbose_name = 'Избранное'

    def ready(self):
        import folders.signals
