from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'


    # Django recommends doing the imports this way to avoid bad things regarding imports
    def ready(self):
        import users.signals
