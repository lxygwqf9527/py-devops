# -*- coding: utf-8 -*-

from flask import request
from api.resource import APIView
from api.models import Notify

class NotifyView(APIView):
    url_prefix = "/notify"

    def get(self):
        notifies = Notify.get_by(unread=True)
        return self.jsonify(notifies)
    
    def patch(self):
        for notify in Notify.get_by_in_id(request.values['ids'],to_dict=False):
            print(notify)
            notify.update(unread=False)
        
        return self.jsonify(error='')