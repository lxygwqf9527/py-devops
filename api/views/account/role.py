# -*- coding:utf-8 -*-

import json

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
        rid = request.values.get('id', None)
        page_perms = request.values.get('page_perms', None)
        deploy_perms = request.values.get('deploy_perms', None)
        host_perms = request.values.get('host_perms', None)
        role = Role.get_by(id=rid, first=True, to_dict=False)
        if not role:
            return self.jsonify(error='未找到指定角色')
        if  page_perms is not None:
            role.page_perms = json.dumps(page_perms)
            # role.update(page_perms=json.dumps(page_perms))
            # Role.update(**request.values)
        role.save()
        # return self.jsonify(error='')