from flask import request
from api.resource import APIView
from api.models import Notify

class NotifyView(APIView):
    url_prefix = "/notify"

    def get(self):
        notifies = Notify.get_by(unread=True)
        return self.jsonify(notifies)
    
    def patch(self):
        Notify.get_by(fl=request.values['ids'],to_dict=False).update(unread=False)
        
        return self.jsonify(error='')