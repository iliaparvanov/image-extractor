from django.apps import AppConfig

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

scheduler = BackgroundScheduler(executors={"default" : ProcessPoolExecutor(4)})

class ImagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'images'

    def ready(self):
        scheduler.start()
