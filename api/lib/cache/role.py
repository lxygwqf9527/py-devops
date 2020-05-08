# -*- coding:utf-8 -*-

from api.extensions import cache
from api.models.account import Role

class RoleCache(object):
    PREFIX_ID = "Role::id::{0}"
    pass