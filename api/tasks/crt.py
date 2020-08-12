# -*- coding:utf-8 -*-
from flask import current_app

from api.extensions import celery
from api.models.host import Host
from api.libs.ssh import SSH
from api.config.Appsetting import AppSetting

@celery.task(name="ssl.acme.install", queue="devops_queue")
def acme_install_task(host_ids):
    hosts = Host.get_by_in_id(to_dict=False,ids=host_ids)
    private_key = AppSetting.get('private_key')
    for host in hosts:
        cli = SSH(host.hostname, host.port, host.username, private_key)
        code, out = cli.exec_command('echo 1>>/opt/a')
        print(out,'===========')