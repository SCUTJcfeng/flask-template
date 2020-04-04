
from app import celery


@celery.task
def system_notice_task(content):
    print(content)
