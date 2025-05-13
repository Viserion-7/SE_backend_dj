from django.apps import AppConfig
from django.db.models.signals import post_migrate


class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        from .models import Category
        from django.db import connection

        def create_default_categories(sender, **kwargs):
            if 'tasks_category' in connection.introspection.table_names():
                default_categories = ['Personal', 'Work', 'Education', 'Miscellaneous']
                for category_name in default_categories:
                    Category.objects.get_or_create(name=category_name)

        post_migrate.connect(create_default_categories, sender=self)