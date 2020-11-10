# -*- coding:utf-8 -*-

from api.models.account import Role
from api.resource import APIView
from api.libs.utils import AttrDict

class RoleView(APIView):
    url_prefix = "/role"

    def get(self):
        roles = [i.to_dict() for i in Role.query.all()]
        return self.jsonify(data="roles",error="")