from django.apps import AppConfig


class IcoConfig(AppConfig):
    name = 'ico'
    
    def ready(self):
        import ico.signals
        
