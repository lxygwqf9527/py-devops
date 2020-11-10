# -*- coding:utf-8 -*-

from api.models.account import Role

class RoleView(APIView):
    url_prefix = "/role"

    def get(self):
        roles = Role.query().all()
        print(roles)