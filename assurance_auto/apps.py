from django.apps import AppConfig


class AssuranceAutoConfig(AppConfig):
    name = 'assurance_auto'
    def ready(self):
        from jobs import updater
        updater.start()
