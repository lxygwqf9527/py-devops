# -*- coding:utf-8 -*-

import datetime
import six

from api.extensions import db


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


class Model(db.Model, ModelMixin):
    __abstract__ = True
