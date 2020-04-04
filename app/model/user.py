
from app.ext import db
from app.util.time import current_timestamp


class User(db.Model):
    """
    template model
    """
    __table_args__                       = ({'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'})

    STATUS_PASS                          = 'pass'
    STATUS_DELETE                        = 'delete'

    ACCOUNT_TYPE_NORMAL                  = 'normal'
    ACCOUNT_TYPE_VIP                     = 'vip'

    id                                   = db.Column(db.Integer, primary_key=True)
    create_time                          = db.Column(db.Integer, default=current_timestamp)
    update_time                          = db.Column(db.Integer, default=current_timestamp, onupdate=current_timestamp)

    username                             = db.Column(db.String(32), default='')
    gender                               = db.Column(db.Integer, default=0)
    birthday                             = db.Column(db.Date, default=0)
    email                                = db.Column(db.String(128), default='')
    phone                                = db.Column(db.Integer, default=0)
    phone_code                           = db.Column(db.Integer, default=86)
    login_pwd_hash                       = db.Column(db.String(128), default='')
    account_type                         = db.Column(db.String(32), default=ACCOUNT_TYPE_NORMAL)
    status                               = db.Column(db.String(32), default=STATUS_PASS)
    remark                               = db.Column(db.String(32), default='')
