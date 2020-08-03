# -*- coding:utf-8 -*-


from api.extensions import db
from api.libs import Model

class SSLType(Model):
    __tablename__ = 'ssl_type'

    name = db.Column(db.String(20),nullable=True)

    def __str__(self):
        return '<SSLType %r>' self.name
    
class SSL(Model):
    __tablename__ = 'ssl'

    name = db.Column(db.String(20),nullable=True)
    ssl_type

    def __str__(self):
        return '<SSLType %r>' self.name