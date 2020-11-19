# pylint: disable=C0103,W0613,C0111
"""
Tasks for managing users with Fabric.
"""
from __future__ import print_function
# import fileinput
import sys
import csv
import logging as log
from datetime import datetime, timedelta
from invoke import task
# from userctl.runners import create_instance as create_runner
# from userctl.users import Users

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


def init_stats(*args, **kwargs):
    return dict({'begin_time': None})


def parse_line(line, stats, *args, **kwargs):
    log.debug('line: %s', line)

    if stats is None:
        stats = init_stats()

    reader = csv.reader([line], delimiter=',', quotechar='"')
    row = next(reader)

    date = datetime.fromtimestamp(int(row[3]))
    if stats['begin_time'] is None:
        stats['begin_time'] = date
    elapsed = date - stats['begin_time']
    log.debug('elapsed: %s', elapsed)

    request = row[4]
    section = request.split('/')[1]
    if not section in stats:
        stats[section] = 1
    else:
        stats[section] += 1

    return stats


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

    # TODO: use a lib to parse logs?
    # https://lars.readthedocs.io/en/latest/lars.apache.html#examples

    # TODO: deal with header
    # TODO: parse section
    # TODO: try in python7
    # TODO: pure functions
    # TODO: duck typing, small methods
    # TODO: logger
    # TODO: decorators

    stats = init_stats()

    input_ = None
    if file is None:
        input_ = sys.stdin
    else:
        input_ = open(file, 'r')

    with input_ as f:
        for line in f:
            try:
                # lines are not necessarily in order!!!
                stats = parse_line(line, stats)
                log.debug('stats: %s', stats)
            except Exception as e:
                log.error('err: %s', e)
    print('done')
