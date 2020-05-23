from flask import request
from api.resource import APIView
from api.models import Notify

class NotifyView(APIView):
    url_prefix = "/notify"

    def get(self):
        notifies = Notify.get_by(unread=True)
        return self.jsonify(notifies)
    
    def patch(self):
        res = Notify.get_by(fl=request.values['ids'],to_dict=False)
        # res = Notify.query.filter(Notify.id.in_(request.values['ids']))

        print(res)
        return self.jsonify(error='')