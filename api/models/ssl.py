# -*- coding:utf-8 -*-


from api.extensions import db
from api.libs import Model
from api.libs import human_datetime

# class SSLType(Model):
#     __tablename__ = 'ssl_type'

#     name = db.Column(db.String(20),nullable=True)

#     def __str__(self):
#         return '<SSLType %r>' self.name
    
class SSL(Model):
    __tablename__ = 'ssls'

    name = db.Column(db.String(20),nullable=False)
    ssl_type = db.Column(db.String(50))
    cer = db.Column(db.Text)
    key = db.Column(db.Text)

    create_at = db.Column(db.String(20), default=human_datetime)
    deleted_at = db.Column(db.String(20))
    expiration =  db.Column(db.String(20), nullable=True)


    def __str__(self):
        return '<SSL %r>' % self.name