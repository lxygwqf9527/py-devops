# -*- coding:utf-8 -*-

from flask import request

from api.models.monitor import Detection
from api.resource import APIView

class Monitor(APIView):

    url_prefix = "/monitor"

    def get(self):
        detections = Detection.query.all()
        return self.jsonify(detections)
        