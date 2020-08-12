# -*- coding:utf-8 -*-
from flask import current_app

from api.extensions import celery
from api.models.host import Host
from api.libs.utils import AppSetting

@celery.task
def acme_install_task(host_ids):
    hosts = Host.get_by_in_id(host_ids)
    private_key = AppSetting.get('private_key')
    for i in hosts:
        cli = SSH(hosts.hostname, hosts.port, hosts.username, private_key)
        code, out = cli.exec_command('echo 1>>/opt/a')
        print(code, out,'===========')