# pylint: disable=C0103,W0613,C0111
"""
Tasks for managing users with Fabric.
"""
from __future__ import print_function
from invoke import task
from userctl.runners import create_instance as create_runner
from userctl.users import Users

import fileinput
import sys


# TODO: fix calls to localhost

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
    runner = create_runner('fabric', connection=ctx)
    users = Users(runner=runner)
    # print(users.list_users(**{'fabric_kwargs': {'hide': True}}).strip())
    # print(users.list_users(**{'fabric_kwargs': {'hide': True}}))
    # with fileinput.input() as f:
    #     text = f.read()
    print('file', file)
    input_ = None
    if file is None:
        input_ = sys.stdin
    else:
        input_ = open(file, 'r')
    with input_ as f:
        for line in f:
            print('line:', line.strip())
    print('done')


# @task
# def delete_user(ctx, user):
#     """
#     Deletes a user on the specified host.
#     """
#     runner = create_runner('fabric', connection=ctx)
#     users = Users(runner=runner)
#     users.delete_user(user, **{'fabric_kwargs': {'hide': True}})
#     print("user deleted")
