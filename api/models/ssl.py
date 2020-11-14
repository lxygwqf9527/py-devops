# -*- coding:utf-8 -*-


from api.extensions import db
from api.libs.utils import human_datetime
from api.libs.database import Model

class AcmeDnsType(Model):
    __tablename__ = 'acme_dns_type'

    name = db.Column(db.String(20),nullable=True)

    def __str__(self):
        return '<AcmeDnsType %r>' % self.name

class AcmeDns(Model):
    __tablename__ = 'acme_dns'
    
    user = db.Column(db.String(50),nullable=True)
    key  = db.Column(db.String(50),nullable=True)
    acme_dns_type_id = db.Column(db.Integer, db.ForeignKey('acme_dns_type.id'))
    acme_dns_type = db.relationship('AcmeDnsType', backref=db.backref('acme_dns'), lazy='subquery', foreign_keys=[acme_dns_type_id])

    created_at = db.Column(db.String(20), default=human_datetime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    deleted_at = db.Column(db.String(20), nullable=True)
    deleted_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __str__(self):
        return '<Dns %r>' % self.user

class SSLType(Model):
    __tablename__ = 'ssl_type'

    name = db.Column(db.String(20),nullable=True)

    def __str__(self):
        return '<SSLType %r>' % self.name
    
class SSL(Model):
    __tablename__ = 'ssls'

    name = db.Column(db.String(20),nullable=False)
    ssl_type_id = db.Column(db.Integer, db.ForeignKey('ssl_type.id'))
    ssl_type = db.relationship('SSLType', backref=db.backref('ssl'), lazy='subquery', foreign_keys=[ssl_type_id])
    cer = db.Column(db.Text)
    key = db.Column(db.Text)
    expiration =  db.Column(db.String(20), nullable=True)

    created_at = db.Column(db.String(20), default=human_datetime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    deleted_at = db.Column(db.String(20), nullable=True)
    deleted_by = db.Column(db.Integer, db.ForeignKey('users.id'))

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