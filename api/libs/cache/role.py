# -*- coding:utf-8 -*-

from api.extensions import cache
from api.models.account import Role

class RoleCache(object):
    PREFIX_ID = "Role::id::{0}"
    PREFIX_NAME = "Role::name::{0}"
    
    @classmethod
    def get_by_name(cls,name):
        role = cache.get(cls.PREFIX_NAME.format(name))
        if role is None:
            role = Role.get_by(name=name, first=True, to_dict=False)
            if role is not None:
                cache.set(cls.PREFIX_NAME.format(name), role)
    
    @classmethod
    def get(cls,id):
        role = cache.get(cls.PREFIX_NAME.format(id))
        if role is None:
            role = Role.get_by_id(id)
            if role is not None:
                cache.set(cls.PREFIX_ID.format(rid), role)        