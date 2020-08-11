# -*- coding:utf-8 -*-
from flask import current_app

from api.extensions import celery

@celery.task(name="ssl.acme.install", queue="acme_install")
def acme_install_task(host_ids):
    hosts = Host.get_by_in_id(host_ids)
    private_key = AppSetting.get('private_key')
    for i in hosts:
        cli = SSH(hosts.hostname, hosts.port, hosts.username, private_key)
        code, out = cli.exec_command('echo 1>>/opt/a')
        print(out,'===========')