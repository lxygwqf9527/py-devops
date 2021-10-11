# -*- coding:utf-8 -*-

from api.resource import APIView
from api.models import History


class HistoryView(APIView):
    url_prefix = '/login/history'

    def get(self):
        histories = []
        for item in History.query.all():
            histories.append({
                'nickname': item.user.nickname,
                'ip': item.ip,
                'created_at': item.created_at.split('-', 1)[1],
            })
    return self.jsonify(data='histories')