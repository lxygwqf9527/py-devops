from flask import request

from flask import g
from api.models import Host
from api.extensions import celery
from api.libs.ssh import SSH
from api.resource import APIView

@celery.task(name="ssl.acme.install", queue="acme_install")
def acme_install_task(host_ids):
    hosts = Host.get_by_in_id(host_ids)
    private_key = AppSetting.get('private_key')
    for i in hosts:
        cli = SSH(hosts.hostname, hosts.port, hosts.username, private_key)
        code, out = cli.exec_command('echo 1>>/opt/a')
        print(out,'===========')

class AcmeInstall(APIView):
    url_prefix = ('/acme/install','/acme/status')
    
    def get(self):
        if request.values.get('id'):
            print(request.values)
    
    def post(self):
        
        acme_install_task.apply_async(args=(request.values.get('host_ids'),), queue="acme_install")

        return self.jsonify(error="")

