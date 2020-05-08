# -*- coding:utf-8 -*-

import datetime
import six

from api.extensions import db
from api.libs.exception import CommitException


class ModelMixin(object):
    def to_dict(self):
        res = dict()
        for k in getattr(self, "__table__").columns:
            if not isinstance(getattr(self, k.name), datetime.datetime):
                res[k.name] = getattr(self, k.name)
            else:
                res[k.name] = getattr(self, k.name).strftime('%Y-%m-%d %H:%M:%S')
        return res

    @classmethod
    def get_columns(cls):
        return {k.name: 1 for k in getattr(cls, "__mapper__").c.values()}

class CRUDMixin(ModelMixin):

    def __init__(self, **kwargs):
        super(CRUDMixin, self).__init__(**kwargs)
    
    @classmethod
    def save(self, commit=True, flush=False):
        print(self.to_dict(),'--------------------')
        db.session.add(self)
        try:
            if flush:
                db.session.flush()
            elif commit:
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise CommitException(str(e))

        return self

class SurrogatePK(object):
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Model(db.Model, CRUDMixin, SurrogatePK):
    __abstract__ = True

class CRUDModel(db.Model, CRUDMixin, SurrogatePK):
    __abstract__ = True
