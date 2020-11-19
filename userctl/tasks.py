# pylint: disable=C0103,W0613,C0111
"""
Tasks for managing users with Fabric.
"""
from __future__ import print_function
import sys
import logging as log
from invoke import task
from userctl.runners import create_instance as create_runner
# from userctl.users import Users
from userctl.log_parser import LogParser

# @task
# def add_user(ctx, user, public_key_filename):
#     """
#     Creates a new user on the specified host.
#     """
#     public_key = None
#     with open(public_key_filename, 'r') as f:
#         public_key = f.read().strip()
#     runner = create_runner('fabric', connection=ctx)
#     users = Users(runner=runner)
#     users.create_user(user, public_key, **{'fabric_kwargs': {'hide': True}})
#     print("user added")


@task
def list_users(ctx, file=None):
    """
    Lists users on the specified host.
    """
    # TODO: rename fabric stuff
    runner = create_runner('invoke', connection=ctx)

    # TODO: if the runner is remote, then we don't want to do one line at a
    # time. in that case, take a file name, i guess
    parser = LogParser(runner=runner)
    # print(users.list_users(**{'fabric_kwargs': {'hide': True}}).strip())
    # print(users.list_users(**{'fabric_kwargs': {'hide': True}}))

    # TODO: use a lib to parse logs?
    # https://lars.readthedocs.io/en/latest/lars.apache.html#examples

    # TODO: deal with header
    # TODO: parse section
    # TODO: try in python2.7
    # TODO: pure functions
    # TODO: duck typing, small methods
    # TODO: logger
    # TODO: decorators

    # stats = init_stats()

    # TODO: pass this into the parser

    input_ = None
    if file is None:
        input_ = sys.stdin
    else:
        input_ = open(file, 'r')

    with input_ as f:
        for line in f:
            try:
                # lines are not necessarily in order!!!
                stats = parser.parse_line(line, None)
                log.debug('stats: %s', stats)
            except Exception as e:
                log.error('err: %s', e)

    print('done')
