# -*- coding: utf-8 -*-

from flask import request
from api.resource import APIView
from api.models import App, Host, Task, Detection

class GetStatistic(APIView):
    prefix = '/statistic'

    def get(self):
        data = {
            'app': App.query.count(),
            'host': Host.query.count(),
            'task': Task.query.count(),
            'detection': Detection.query.count()
        }
        return self.jsonify(data)

class GetAlarm(APIView)