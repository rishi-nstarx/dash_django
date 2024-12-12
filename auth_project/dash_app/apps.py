from django.apps import AppConfig
import logging

class DashAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dash_app'

    def ready(self):
        try:
            # Import all Dash app modules
            import dash_app.dash_apps.admission
            import dash_app.dash_apps.admission_explained
            import dash_app.dash_apps.attendence_graph
        except Exception as e:
            logging.error(f"Error loading Dash apps: {e}")
