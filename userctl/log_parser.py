# pylint: disable=W0613, C0111
"""
Parses logs, potentially for different host environments. I wrote this for
Frabric originally, and it could be adapted for remote calls again.
"""

import sys
import csv
import logging as log
import pprint
from datetime import datetime, timedelta

pp = pprint.PrettyPrinter(indent=4)


# TODO: Use a factory for other types of input.
class LogParser(object):
    """
    Log parser for a generic Linux host.
    """

    runner = None
    file = None

    # # self.state
    # {
    #   timestamp:
    #     {
    #       section: count
    #     }
    # }
    state = None

    def __init__(self, *args, **kwargs):
        self.post_initialize(*args, **kwargs)

    def post_initialize(self, *args, **kwargs):
        self.runner = kwargs.get('runner', None)
        self.file = kwargs.get('file', None)

    def run_command(self, cmd, *args, **kwargs):
        return

    @staticmethod
    def init_state(*args, **kwargs):
        return {
            'stats': {
                'begin_time': None,
                'end_time': None,
                # we need to save the last 10 seconds of info...
                # we need to save the last two minutes of info...
                'is_traffic_alerting': False,
                'traffic_alert_datetime': None,
                'traffic_alert_threshold': 10,
                'traffic_alert_duraction_seconds': 120
            },
            'rows': {}
        }

    def get_section(self, text):
        # Hate it.
        path = text.split(' ')[1]
        return path.split('/')[1]

    def get_timestamp(self, row, *args, **kwargs):
        return int(row[3])

    def get_event_time(self, timestamp, *args, **kwargs):
        return datetime.fromtimestamp(timestamp)

    def update_state(self, state, event_time, section, *args, **kwargs):
        # inc the count for the event time and section
        if not event_time in state['rows'].keys():
            state['rows'][event_time] = {
                section: 1
            }
        else:
            if not section in state['rows'][event_time].keys():
                state['rows'][event_time][section] = 1
            else:
                state['rows'][event_time][section] += 1
        return state

    def remove_old_rows(self, state, alert_time, *args, **kwargs):
        state['rows'] = {k: v for (k, v) in state['rows'].items()
                         if k >= alert_time}
        return state

    def get_total_requests(self, *args, **kwargs):
        # for event_time in self.state['rows'].keys():
        total_requests = 0
        for event_time in self.state['rows']:
            for section in self.state['rows'][event_time]:
                total_requests += self.state['rows'][event_time][section]
        return total_requests

    def parse_line(self, line, *args, **kwargs):
        log.debug('line: %s', line)
        delimiter = kwargs.get('delimiter', ',')
        quotechar = kwargs.get('quotechar', '"')

        reader = csv.reader([line], delimiter=delimiter, quotechar=quotechar)
        row = next(reader)

        # For every 10 seconds of log lines, display stats about the traffic
        # during those 10 seconds: the sections of the web site with the most hits
        # * strategy 1: assume they are in order and then make adjustments

        # Whenever total traffic for the past 2 minutes exceeds a certain number on
        # average, print a message to the console saying that “High traffic
        # generated an alert - hits = {value}, triggered at {time}”. The default
        # threshold should be 10 requests per second but should be configurable.

        # 2. 2 minutes (configurable)
        # 1. 10 seconds (configurable)
        # 3. unit tests
        # 4. docs

        timestamp = self.get_timestamp(row)
        event_time = self.get_event_time(timestamp)
        stats_time = event_time - timedelta(seconds=10)
        alert_time = event_time - timedelta(seconds=120)
        section = self.get_section(row[4])

        self.state = self.update_state(self.state, event_time, section)

        self.state = self.remove_old_rows(self.state, alert_time)
        total_requests = self.get_total_requests()
        # The default threshold should be 10 requests per second
        # 2 minutes = 120 seconds = 10 * 120 == 1200 requests
        print('total_requests', total_requests)

        stats_rows = {
            k: v for (k, v) in self.state['rows'].items()
            if k >= stats_time
        }

        pp.pprint('stats state: {}'.format(stats_rows))
        # The default threshold should be 10 requests per second (for 2 minutes (configurable))

        return self.state

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

        # TODO: kwargs.get('parse_args', {})

        self.state = LogParser.init_state()

        # TODO: throwaway header

        input_ = None
        if self.file is None:
            input_ = sys.stdin
        else:
            input_ = open(self.file, 'r')

        with input_ as file:
            for line in file:
                try:
                    self.parse_line(line, None)
                # pylint: disable=broad-except
                except Exception as err:
                    log.error('err: %s', err)

        pp.pprint(self.state)
