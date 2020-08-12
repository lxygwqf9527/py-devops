from flask import request, current_app

from api.models import Host
from api.tasks.crt import acme_install_task
from api.libs.ssh import SSH
from api.resource import APIView



class AcmeInstall(APIView):
    url_prefix = ('/acme/install','/acme/status')
    
    def get(self):
        if request.values.get('id'):
            print(request.values)
    
    def post(self):
        # acme_install_task.delay(request.values.get('host_ids'))
        acme_install_task.apply_async(args=(request.values.get('host_ids'),))
        current_app.logger.info("acme install host_ids: %s" % request.values.get('host_ids'))
        return self.jsonify(error="")

