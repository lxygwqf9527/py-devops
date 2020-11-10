# -*- coding:utf-8 -*-

import os

from flask import Blueprint
from flask_restful import Api

from api.resource import register_resources

HERE = os.path.abspath(os.path.dirname(__file__))

# account
blueprint_account_v1 = Blueprint('account_api_v1', __name__, url_prefix='/api/v1/account')
account_rest = Api(blueprint_account_v1)
register_resources(os.path.join(HERE, "account"), account_rest)

# home
blueprint_home_v1 = Blueprint('home_api_v1', __name__, url_prefix='/api/v1/home')
home_rest = Api(blueprint_home_v1)
register_resources(os.path.join(HERE, "home"), home_rest)

# host
blueprint_host_v1 = Blueprint('host_api_v1', __name__, url_prefix='/api/v1/host/')
host_rest = Api(blueprint_host_v1)
register_resources(os.path.join(HERE, "host"), host_rest)

# ssl
blueprint_ssl_v1 = Blueprint('ssl_api_v1', __name__, url_prefix='/api/v1/ssl')
ssl_rest = Api(blueprint_ssl_v1)
register_resources(os.path.join(HERE, "crt"), ssl_rest)

# url_prefix = url_prefix = ("/ci/flush", "/ci/<int:ci_id>/flush") 其他用法