
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

celery = None
db = SQLAlchemy()
migrate = Migrate()

__all__ = (
    'db',
    'migrate',
)
