# pylint: disable=W0613,C0111
"""
User managers implemented for different host environments.
"""
# from userctl.utils import load_platform_subclass

import sys
import csv
import logging as log
from datetime import datetime, timedelta


class LogParser(object):
    """
    User manager for a generic Linux host.
    """

    # PASSWD_USERNAME = 0
    # PASSWD_PASSWORD = 1
    # PASSWD_UID = 2
    # PASSWD_GID = 3
    # PASSWD_COMMENT = 4
    # PASSWD_HOME = 5
    # PASSWD_SHELL = 6

    # platform = 'Linux'
    # distribution = None
    runner = None
    state = None

    # def __new__(cls, *args, **kwargs):
    #     # """
    #     # Returns a subclass matching the platform and distribution.
    #     # """
    #     # return load_platform_subclass(Users, *args, **kwargs)
    #     pass

    def __init__(self, *args, **kwargs):
        self.post_initialize(*args, **kwargs)

    def post_initialize(self, *args, **kwargs):
        self.runner = kwargs.get('runner', None)

    def run_command(self, cmd, *args, **kwargs):
        return

    @staticmethod
    def init_stats(*args, **kwargs):
        return dict({'begin_time': None})

    @staticmethod
    def init_state(*args, **kwargs):
        return dict({
            'stats': LogParser.init_stats()
        })

    def parse_line(self, line, stats, *args, **kwargs):
        log.debug('line: %s', line)

        delimiter = kwargs.get('delimiter', ',')
        quotechar = kwargs.get('quotechar', '"')

        if self.state is None:
            self.state = LogParser.init_state()

        reader = csv.reader([line], delimiter=delimiter, quotechar=quotechar)
        row = next(reader)

        # For every 10 seconds of log lines, display stats about the traffic
        # during those 10 seconds: the sections of the web site with the most hits
        # * strategy 1: assume they are in order and then make adjustments

        # Whenever total traffic for the past 2 minutes exceeds a certain number on
        # average, print a message to the console saying that “High traffic
        # generated an alert - hits = {value}, triggered at {time}”. The default
        # threshold should be 10 requests per second but should be configurable.

        date = datetime.fromtimestamp(int(row[3]))
        if self.state['stats']['begin_time'] is None:
            self.state['stats']['begin_time'] = date
        elapsed = date - self.state['stats']['begin_time']
        log.debug('elapsed: %s', elapsed)

        request = row[4]
        section = request.split('/')[1]
        if not section in self.state['stats']:
            self.state['stats'][section] = 1
        else:
            self.state['stats'][section] += 1

        return self.state['stats']
