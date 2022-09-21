from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import status_schedule
def start():
	scheduler = BackgroundScheduler()
	scheduler.add_job(status_schedule, 'interval', seconds=1440)
	scheduler.start()