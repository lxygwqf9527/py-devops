# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from flask import request
from sqlalchemy import and_

from api.libs import human_datetime
from api.resource import APIView
from api.models import App, Host, Task, Detection, Alarm

class GetStatistic(APIView):
    '''
        获取总览数据，app，host，task，detection
    '''
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
    '''
        home获取报警函数
    '''
    url_prefix = '/alarm'

    def get(self):
        now = datetime.now()

        data = {human_datetime(now - timedelta(days=x + 1)): 0 for x in range(14)}
        # 获取十四天以内的报警
        for alarm in Alarm.query.filter(and_(Alarm.status == 1, Alarm.created_at.__gt__(human_datetime(now - timedelta(days=14))))):
            date = alarm.created_at[:10]
            if date in str(data.keys()):
                data[date] += 1
        data = [{'date': k, 'value': v} for k, v in data.items()]
        return self.jsonify(data)