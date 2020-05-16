from flask import request
from api.resource import APIView
from api.models.account import Notify

class NotifyView(APIView):
    url_prefix = "/notify"

    def get(self):
        notifies = Notify.get_by(unread=True)
        return self.jsonify(notifies)
    
    def patch(self):
        
        Notify.ofilter(id__in=form.ids).update(unread=False)
        return self.jsonify(error=error)