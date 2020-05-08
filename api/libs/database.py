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
        return res.pop('_sa_instance_state', None)

    @classmethod
    def get_columns(cls):
        return {k.name: 1 for k in getattr(cls, "__mapper__").c.values()}

class CRUDMixin(ModelMixin):

    def __init__(self, **kwargs):
        super(CRUDMixin, self).__init__(**kwargs)
    
    def update(self, flush=False, **kwargs):
        kwargs.pop("id", None) # id不需要更新，所以刨除id
        for attr, value in six.iteritems(kwargs):
            #print(attr,value,'==============')
            if value is not None:
                setattr(self, attr, value)
        if flush:
            return self.save(flush=flush)
        return self.save()
    
    @classmethod
    def save(self, commit=True, flush=False):
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

    @classmethod
    def get_by(cls, first=False, to_dict=True, fl=None, exclude=None, deleted=False, use_master=False, **kwargs):
        db_session = db.session if not use_master else db.session().using_bind("master")
        fl = fl.strip().split(",") if fl and isinstance(fl, six.string_types) else (fl or [])
        exclude = exclude.strip().split(",") if exclude and isinstance(exclude, six.string_types) else (exclude or [])

        keys = cls.get_columns()
        fl = [k for k in fl if k in keys]
        fl = [k for k in keys if k not in exclude and not k.isupper()] if exclude else fl
        fl = list(filter(lambda x: "." not in x, fl))

        if hasattr(cls, "deleted") and deleted is not None:
            kwargs["deleted"] = deleted

        if fl:
            query = db_session.query(*[getattr(cls, k) for k in fl])
            query = query.filter_by(**kwargs)
            result = [{k: getattr(i, k) for k in fl} for i in query]
        else:
            result = [i.to_dict() if to_dict else i for i in getattr(cls, 'query').filter_by(**kwargs)]

        return result[0] if first and result else (None if first else result)

class SurrogatePK(object):
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Model(db.Model, CRUDMixin, SurrogatePK):
    __abstract__ = True

class CRUDModel(db.Model, CRUDMixin, SurrogatePK):
    __abstract__ = True
