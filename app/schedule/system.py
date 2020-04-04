
from app import celery
from app.util.time import current_timestamp


@celery.task
def test_schedule():
    print(f'test_schedule: {current_timestamp()}')
