# -*- coding:utf-8 -*-


from api.extensions import db
from api.libs.utils import Model
from api.libs.utils import human_datetime

class SSLType(Model):
    __tablename__ = 'ssl_type'

    key = db.Column(db.String(20),nullable=True)
    value = db.Column(db.Text)

    def __str__(self):
        return '<SSLType %r>' % self.key
    
class SSL(Model):
    __tablename__ = 'ssls'

    name = db.Column(db.String(20),nullable=False)
    ssl_type_id = db.Column(db.Integer, db.ForeignKey('ssl_type.id'))
    ssl_type = db.relationship('SSLType', backref=db.backref('ssl'), lazy='subquery', foreign_keys=[ssl_type_id])
    cer = db.Column(db.Text)
    key = db.Column(db.Text)

    create_at = db.Column(db.String(20), default=human_datetime)
    deleted_at = db.Column(db.String(20))
    expiration =  db.Column(db.String(20), nullable=True)


    def __str__(self):
        return '<SSL %r>' % self.name

class SSLSetting(Model):
    __tablename__ = 'ssl_setting'

    key = db.Column(db.String(50), unique=True)
    value = db.Column(db.Text)
    desc = db.Column(db.String(255), nullable=True)

    ssl_type_id = db.Column(db.Integer, db.ForeignKey('ssl_type.id'))
    ssl_type = db.relationship('SSLType', backref=db.backref('ssl_setting'), lazy='subquery', foreign_keys=[ssl_type_id])

    def __str__(self):
        return '<Setting %r>' % self.key