# -*- coding:utf-8 -*-

from api.models.account import Role
from api.resource import APIView
from api.libs.utils import AttrDict

class RoleView(APIView):
    url_prefix = "/role"

    def get(self):
        roles = Role.query.all()
        roles = AttrDict(roles=roles)
        print(roles)
        return self.jsonify(error="")