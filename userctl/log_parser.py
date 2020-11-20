# pylint: disable=W0613, C0111
"""
Parses logs, potentially for different host environments.
"""
# from userctl.utils import load_platform_subclass

import sys
import csv
import logging as log
from datetime import datetime  # , timedelta


class LogParser(object):
    """
    Log parser for a generic Linux host.
    """

    # platform = 'Linux'
    # distribution = None
    runner = None
    file = None
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
        self.file = kwargs.get('file', None)

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

    def parse_line(self, line, *args, **kwargs):
        log.debug('line: %s', line)

        delimiter = kwargs.get('delimiter', ',')
        quotechar = kwargs.get('quotechar', '"')

        # if self.state is None:
        #     self.state = LogParser.init_state()

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

    def parse(self, *args, **kwargs):
        # TODO: use a lib to parse logs?
        # https://lars.readthedocs.io/en/latest/lars.apache.html#examples
        # TODO: deal with header
        # TODO: parse section
        # TODO: try in python2.7
        # TODO: pure functions
        # TODO: duck typing, small methods
        # TODO: logger
        # TODO: decorators
        # TODO: unit tests

        self.state = LogParser.init_state()

        input_ = None
        if self.file is None:
            input_ = sys.stdin
        else:
            input_ = open(self.file, 'r')

        with input_ as file:
            for line in file:
                try:
                    # lines are not necessarily in order!!!
                    stats = self.parse_line(line, None)
                    log.debug('stats: %s', stats)
                # pylint: disable=broad-except
                except Exception as err:
                    log.error('err: %s', err)
