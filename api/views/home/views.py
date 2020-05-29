# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from flask import request

from api.libs import human_datetime
from api.resource import APIView
from api.models import App, Host, Task, Detection, Alarm

class GetStatistic(APIView):
    url_prefix = '/statistic'

    def get(self):
        data = {
            'app': App.query.count(),
            'host': Host.query.count(),
            'task': Task.query.count(),
            'detection': Detection.query.count()
        }
        return self.jsonify(data)

class GetAlarm(APIView):
    url_prefix = '/alarm'

    def get(self):
        now = datetime.now()

        data = {human_date(now - timedelta(days=x + 1)): 0 for x in range(14)}
        for alarm in Alarm.get_by(status='1', created_at > human_date(now - timedelta(days=14))):

