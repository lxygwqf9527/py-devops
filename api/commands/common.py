# -*- coding: utf-8 -*-
"""Click commands."""


import click
from flask.cli import with_appcontext
from api.extensions import db
from api.libs.perm.crud.user import UserCRUD



@click.command()
@with_appcontext
def db_setup():
    """create tables
    """
    db.create_all()

@click.command()
@click.option(
    '-u',
    '--user',
    help='username'
)
@click.option(
    '-p',
    '--password',
    help='password'
)
@click.option(
    '-m',
    '--mail',
    help='mail'
)
@click.option(
    '--is_admin',
    is_flag=True
)
@with_appcontext
def add_user(user, password, mail, is_admin):
    """
    create a user

    is_admin: default is False

    Example:  flask add-user -u <username> -p <password> -m <mail>  [--is_admin]
    """
    assert user is not None
    assert password is not None
    assert mail is not None
    
    UserCRUD.add(username=user, password=password, email=mail, is_supper=is_admin)