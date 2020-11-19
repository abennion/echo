# pylint: disable=C0103,W0613,C0111
"""
Tasks for managing users with Fabric.
"""
from __future__ import print_function
# import fileinput
import sys
import csv
from datetime import datetime, timedelta
from invoke import task
# from userctl.runners import create_instance as create_runner
# from userctl.users import Users

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
    # runner = create_runner('fabric', connection=ctx)
    # users = Users(runner=runner)
    # print(users.list_users(**{'fabric_kwargs': {'hide': True}}).strip())
    # print(users.list_users(**{'fabric_kwargs': {'hide': True}}))
    # with fileinput.input() as f:
    #     text = f.read()
    print('file', file)

    # TODO: use a lib to parse logs?
    # https://lars.readthedocs.io/en/latest/lars.apache.html#examples

    # "remotehost","rfc931","authuser","date","request","status","bytes"
    # "10.0.0.2","-","apache",1549573860,"GET /api/user HTTP/1.0",200,1234
    # "10.0.0.4","-","apache",1549573860,"GET /api/user HTTP/1.0",200,1234
    # "10.0.0.4","-","apache",1549573860,"GET /api/user HTTP/1.0",200,1234
    # "10.0.0.2","-","apache",1549573860,"GET /api/help HTTP/1.0",200,1234

    # TODO: deal with header
    # TODO: parse section

    # epoch to datetime
    print('datetime', datetime.fromtimestamp(1549573860))

    # TODO: pure functions
    # TODO: duck typing, small methods
    # TODO: logger

    begin_time = None
    next_begin_time = None

    input_ = None
    if file is None:
        input_ = sys.stdin
    else:
        input_ = open(file, 'r')
    with input_ as f:
        for line in f:
            try:
                # TODO: call parse_line(...)
                print('line0', line.strip())
                reader = csv.reader([line], delimiter=',', quotechar='"')
                row = next(reader)
                date = datetime.fromtimestamp(int(row[3]))
                if begin_time is None:
                    begin_time = date
                elapsed = date - begin_time
                print('elapsed', elapsed)
                request = row[4]
                section = request.split('/')[1]
                print(
                    'date:', date,
                    ', request:', request,
                    ', section:', section
                )
            except Exception as e:
                print(e)
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
