from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .views import *

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    # 일일 리소스별 비용 디비에 저장 : 당일 저녁 6시
    scheduler.add_job(save_data_to_db, 'cron', hour=18)

    # 일일 전체 비용 디비에 저장 : 당일 저녁 6시
    scheduler.add_job(daily_usage, 'cron', hour=18)

    # 한 달 전체 비용 디비에 저장 : 한 달의 마지막 날 저녁 9시
    scheduler.add_job(monthly_usage, 'cron', day='last', hour=21)

    def auto_save_data():
        save_data_to_db()
        daily_usage()
        monthly_usage()

    scheduler.start()
