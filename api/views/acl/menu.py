# -*- coding:utf-8 -*-

from flask import request
from api.lib.perm.acl.permission import PermissionCRUD
from api.resource import APIView

class MenuPermissionView(APIView):
    url_prefix = "/menu/<int:role_id>/permissions"

    def get(self, role_id=None):
        return self.jsonify(PermissionCRUD.get_all(role_id))
    
    def options(self,role_id=None):
        print(role_id)