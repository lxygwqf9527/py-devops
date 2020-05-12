# -*- coding:utf-8 -*-

import copy
import hashlib
import json
from datetime import datetime

from flask import current_app
from flask_sqlalchemy import BaseQuery


from api.extensions import db
from api.libs import Model, CRUDModel
from api.libs.utils import human_datetime




class UserQuery(BaseQuery):
    def _join(self, *args, **kwargs):
        super(UserQuery, self)._join(*args, **kwargs)

    def authenticate(self, login, password):
        '''
            根据username或者email当用户
        '''
        user = self.filter(db.or_(User.username == login,
                                  User.email == login)).first()
        if user:
            current_app.logger.info(user)
            authenticated = user.check_password(password)
        else:
            authenticated = False
            
        return user, authenticated

    def get_by_username(self, username):
        '''
            根据username查询
        '''
        user = self.filter(User.username == username).filter(User.deleted_by.is_(None)).first()

        return user

    def get_by_nickname(self, nickname):
        '''
            根据nickname查询
        '''
        user = self.filter(User.nickname == nickname).filter(User.deleted_by.is_(None)).first()

        return user

    def get(sefl, id):
        '''
            根据id查询
        '''

        user = self.filter(User.id == id).filter(User.deleted_by.is_(None)).first()

        return copy.deepcopy(user)

class User(Model):
    __tablename__ = 'users'
    query_class = UserQuery

    username = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(32), unique=True)
    nickname = db.Column(db.String(20), nullable=True)
    _password = db.Column("password", db.String(80))
    type = db.Column(db.String(20), default='default')
    is_supper = db.Column(db.Boolean,default=False)
    is_active = db.Column(db.Boolean,default=True)
    access_token = db.Column(db.String(32))
    token_expired = db.Column(db.Integer, nullable=True)
    last_login = db.Column(db.String(20))
    last_ip = db.Column(db.String(50))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)

    created_at = db.Column(db.String(20), default=human_datetime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    deleted_at = db.Column(db.String(20), nullable=True)
    deleted_by = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=True)


    def __str__(self):
        return self.username
    
    def get_id(self):
        return self.id
    
    @staticmethod
    def is_authenticated():
        return True
    
    def _get_password(self):
        return self._password
    
    def _set_password(self, password):
        self._password = hashlib.md5(password.encode('utf-8')).hexdigest()
    
    password = db.synonym("_password", descriptor=property(_get_password, _set_password))

    def check_password(self, password):

        if self.password is None:
            return False
        return self.password == password

    @property
    def page_perms(self):
        print(role)
        if self.role and self.role.page_perms:
            data = []
            perms = json.loads(self.role.page_perms)
            for m, v in perms.items():
                for p, d in v.items():
                    data.extend(f'{m}.{p}.{x}' for x in d)
            return data
        else:
            return []

    @property
    def deploy_perms(self):
        perms = json.loads(self.role.deploy_perms) if self.role.deploy_perms else {}
        perms.setdefault('apps', [])
        perms.setdefault('envs', [])
        return perms
    
    def has_perms(self, codes):
        # return self.is_supper or self.role in codes
        return self.is_supper

class Role(CRUDModel):
    __tablename__ = "roles"

    name = db.Column(db.String(50))
    desc = db.Column(db.String(255), nullable=True)
    page_perms = db.Column(db.Text, nullable=True)
    deploy_perms = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.String(20), default=human_datetime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('Users',backref=db.backref('role'), lazy='dyamic')

    def to_dict(self, *args, **kwargs):
        tmp = super().to_dict(*args, **kwargs)
        tmp['page_perms'] = json.loads(self.page_perms) if self.page_perms else None
        tmp['deploy_perms'] = json.loads(self.deploy_perms) if self.deploy_perms else None
        # tmp['used'] = self.user_set.count()
        return tmp
    
    def __str__(self):
        return self.name
    
    def count(self):
        pass
