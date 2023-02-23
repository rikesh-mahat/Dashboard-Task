from django.apps import AppConfig


class SubisuConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subisu'
    
    
    def ready(self):
        import subisu.signals  # singal lai register gareko
