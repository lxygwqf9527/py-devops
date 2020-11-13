# -*- coding:utf-8 -*-

from api.models.account import Role
from api.resource import APIView
from api.libs.utils import AttrDict
from flask import request

class RoleView(APIView):
    url_prefix = "/role"

    def get(self):
        roles = [i.to_dict() for i in Role.query.all()]
        return self.jsonify(roles)
    
    def patch(self):
        print(request.values)