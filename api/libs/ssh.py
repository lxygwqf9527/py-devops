# -*- coding: utf-8 -*-

from paramiko.client import SSHClient, AutoAddPolicy
from paramiko.config import SSH_PORT
from paramiko.ssh_exception import AuthenticationException
from io import StringIO

class SSH:
    def __init__(self, hostname, port=SSH_PORT, username='root', pkey=None, password=None, connect_timeout=10):
        if pkey is None and password is None:
            raise Exception('public key and password must have one is not None')
        self.client = None
        self.arguments = {
            'hostname': hostname,
            'port': port,
            'username': username,
            'password': password,
            'pkey': RSAKey.from_private_key(StringIO(pkey)) if isinstance(pkey, str) else pkey,
            'timeout': connect_timeout,
        }