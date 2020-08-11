# -*- coding:utf-8 -*-
from api.extensions import celery
from flask import current_app

@celery.task(name="ssl.acme.install", queue="acme_install")
def acme_install_task(host_ids):
    current_app.logger.info("acme install host_ids:", host_ids)
    hosts = Host.get_by_in_id(host_ids)
    private_key = AppSetting.get('private_key')
    for i in hosts:
        cli = SSH(hosts.hostname, hosts.port, hosts.username, private_key)
        code, out = cli.exec_command('echo 1>>/opt/a')
        print(out,'===========')