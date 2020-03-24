# -*- coding:utf-8 -*-



class RoleCache(object):
    PREFIX_ID = "Role::id::{0}"
    PREFIX_NAME = "Role::app_id::{0}::name::{1}"

    @classmethod
    def get_by_name(cls, app_id, name):
        role = cache.get(cls.PREFIX_NAME.format(app_id, name))
        if role is None:
            role = Role.get_by(app_id=app_id, name=name, first=True, to_dict=False)
            if role is not None:
                cache.set(cls.PREFIX_NAME.format(app_id, name), role)

        return role

    @classmethod
    def get(cls, rid):
        role = cache.get(cls.PREFIX_ID.format(rid))
        if role is None:
            role = Role.get_by_id(rid)
            if role is not None:
                cache.set(cls.PREFIX_ID.format(rid), role)

        return role