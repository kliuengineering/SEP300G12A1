from django.apps import AppConfig

# configuration is inherited from the AppConfig class
class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mainapp'
