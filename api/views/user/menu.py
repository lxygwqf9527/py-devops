# -*- coding:utf-8 -*-

from flask import request

from api.resource import APIView

class MenuPermissionView(APIView):
    url_prefix = "/menu/<int:role_id>/permissions"

    def get(self, role_id=None):
        return abort(1,'你好')