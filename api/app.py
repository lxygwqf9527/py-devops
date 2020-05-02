# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import os
import sys
from inspect import getmembers
from logging.handlers import RotatingFileHandler
from logging.config import dictConfig

# from api.flask_cas import CAS
from flask import Flask
from flask import make_response, jsonify
from flask.blueprints import Blueprint
from flask.cli import click

import api.views

from api.extensions import (
    bcrypt,
    cors,
    cache,
    db,
    login_manager,
    migrate,
    celery,
    # rd,
    # es
)

from .models.account import User

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
API_PACKAGE = "api"

def create_app(config_object="settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    # register_error_handlers(app)
    # register_shell_context(app)
    register_commands(app)
    configure_logger(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    cors.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    # rd.init_app(app)
    # if app.config.get("USE_ES"):
    #     es.init_app(app)
    celery.conf.update(app.config)

def register_blueprints(app):
    for item in getmembers(api.views):
        if item[0].startswith("blueprint") and isinstance(item[1], Blueprint):
            app.register_blueprint(item[1])

# def register_error_handlers(app):
#     """Register error handlers."""
#     def render_error(error):
#         """Render error template."""
#         import traceback
#         app.logger.error(traceback.format_exc())
#         error_code = getattr(error, "code", 500)
#         return make_response(jsonify(message=str(error)), error_code)

# def register_shell_context(app):
#     """Register shell context objects."""

#     def shell_context():
#         """Shell context objects."""
#         return {"db": db, "User": User}

#     app.shell_context_processor(shell_context)

def register_commands(app):
    """Register Click commands."""
    for root, _, files in os.walk(os.path.join(HERE, "commands")):
        for filename in files:
            if not filename.startswith("_") and filename.endswith("py"):
                module_path = os.path.join(API_PACKAGE, root[root.index("commands"):])
                if module_path not in sys.path:
                    sys.path.insert(1, module_path)
                command = __import__(os.path.splitext(filename)[0])
                func_list = [o[0] for o in getmembers(command) if isinstance(o[1], click.core.Command)]
                for func_name in func_list:
                    app.cli.add_command(getattr(command, func_name))

def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(pathname)s %(lineno)d - %(message)s")

    if app.debug:
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)

    log_file = app.config['LOG_PATH']
    file_handler = RotatingFileHandler(log_file,
                                       maxBytes=2 ** 30,
                                       backupCount=7)
    file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))