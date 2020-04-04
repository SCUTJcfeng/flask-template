
import traceback
from flask import Flask
from flask import request
from flask import g
from flask import current_app
from app.ext import celery
from app.ext import db
from app.api import init_blueprint as _config_blueprint


def create_app():
    app = Flask(__name__)
    _config_app(app)
    _config_logging(app)
    _config_ext(app)
    _config_handler(app)
    _config_blueprint(app)
    return app


def _config_app(app):
    app.config.from_object('app.config.production')
    try:
        app.config.from_object('app.config.test')
    except:
        pass


def _config_logging(app):
    from flask.logging import default_handler
    import logging

    formatter = logging.Formatter(
        '%(asctime)s %(name)s %(levelname)s request: %(request_id)s ip: %(ip)s %(filename)s:'
        '%(funcName)s:%(lineno)d %(message)s')
    default_handler.setFormatter(formatter)
    logger = logging.getLogger(app.import_name)
    if app.debug and not logger.level:
        logger.setLevel(logging.DEBUG)
    app.logger = logger


def _config_ext(app):
    _config_ext_celery(app)
    _config_ext_db(app)
    _config_ext_migrate(app)


def _config_ext_celery(app):
    from celery import Celery

    global celery
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config.get('CELERY_RESULT_BACKEND', None)
    )
    celery.config_from_object('app.config.celery_conf')
    task = celery.Task

    class ContextTask(task):
        def __call__(self, *_args, **_kwargs):
            with app.app_context():
                return task.__call__(self, *_args, **_kwargs)

        def on_failure(self, exc, task_id, args, kwargs, einfo):
            from app.task.system import system_notice_task
            task_info_str = "task_name => %s, args => %s, kwargs => %s" % (
                self.name, args, kwargs)
            err_str = traceback.format_exc()
            err_str = "\n".join([task_info_str, err_str])
            system_notice_task.delay(err_str.replace('\n', '<br>'))

    setattr(ContextTask, 'abstract', True)
    setattr(celery, 'Task', ContextTask)


def _config_ext_db(app):
    db.init_app(app)


def _config_ext_migrate(app):
    from app.ext import migrate

    migrate.init_app(app, db)


def _config_handler(app):
    @app.before_request
    def before_request():
        _setup_lang()

    @app.errorhandler(Exception)
    def handle_exception(e):
        import traceback
        from app.util.response import response_error
        from app.task import system_notice_task

        system_notice_task.delay(traceback.format_exc())
        return response_error(msg=str(e))

    def _setup_lang():
        support_lang_list = current_app.config['SUPPORT_LANG_LIST']
        g.lang = current_app.config['DEFAULT_LANG']
        accept_languages = request.accept_languages.values()
        for accept_language in accept_languages:
            if accept_language in support_lang_list:
                g.lang = accept_language
                break
