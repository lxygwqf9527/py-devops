from flask import request

from flask import current_app
from autoapp import app
from api.models import Host
from api.extensions import celery
from api.libs.ssh import SSH
from api.resource import APIView

@celery.task
def acme_install_task(host_ids):
    with app.app_context():
        hosts = Host.get_by_in_id(host_ids)
        print(hosts,'----------')

class AcmeInstall(APIView):
    url_prefix = ('/acme/install','/acme/status')
    
    def get(self):
        if request.values.get('id'):
            print(request.values)
    
    def post(self):
        
        acme_install_task.delay(request.values.get('host_ids'))

        return self.jsonify(error="")

