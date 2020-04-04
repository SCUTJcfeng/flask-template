
from celery.schedules import crontab
from kombu import Exchange, Queue
from app.const.celery import *

task_serializer = 'json'
accept_content = ['json']  # Ignore other content
result_serializer = 'json'
timezone = 'Asia/Shanghai'
enable_utc = True

task_default_queue = QUEUE_DEFAULT
task_default_exchange_type = EXCHANGE_TYPE_DIRECT
task_default_routing_key = 'default_task'

imports = {
    'app.task',
    'app.schedule',
}

beat_schedule = {
    'test_schedule': {
        'task': 'app.schedule.system.test_schedule',
        'schedule': crontab('*/1')
    }
}

task_routes = {
    'app.task.system.*': {'queue': QUEUE_SYSTEM, 'routing_key': ROUTING_KEY_SCHEDULE},
    'app.schedule.system.*': {'queue': QUEUE_SCHEDULE, 'routing_key': ROUTING_KEY_SYSTEM}
}

exchange_system = Exchange(EXCHANGE_SYSTEM, type=EXCHANGE_TYPE_DIRECT)
exchange_schedule = Exchange(EXCHANGE_SCHEDULE, type=EXCHANGE_TYPE_DIRECT)

task_queues = (
    Queue(QUEUE_SYSTEM, exchange=exchange_system, routing_key=ROUTING_KEY_SYSTEM),
    Queue(QUEUE_SCHEDULE, exchange=exchange_schedule, routing_key=ROUTING_KEY_SCHEDULE),
)
