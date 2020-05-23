from flask import request
from api.resource import APIView
from api.models import Notify

class NotifyView(APIView):
    url_prefix = "/notify"

    def get(self):
        notifies = Notify.get_by(unread=True)
        return self.jsonify(notifies)
    
    def patch(self):
        print(request.values['ids'])
        res = Notify.query.filter(Notify.id.in_(request.values['ids']))
        
        print(res)
        return self.jsonify(error='')