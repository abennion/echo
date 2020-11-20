# pylint: disable=W0613, C0111
"""
Parses logs, potentially for different host environments. I wrote this for
Frabric originally. It could be adapted for remote calls.
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
    state = None
    traffic_alert_minutes = 2
    traffic_alert_requests_per_minute = 10
    stats_seconds = 10

    def __init__(self, *args, **kwargs):
        self.post_initialize(*args, **kwargs)

    def post_initialize(self, *args, **kwargs):
        self.runner = kwargs.get('runner', None)
        self.file = kwargs.get('file', None)

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

    def get_section(self, row, col, *args, **kwargs):
        # Hate it.
        text = row[col]
        path = text.split(' ')[1]
        return path.split('/')[1]

    def get_timestamp(self, row, col, *args, **kwargs):
        return int(row[col])

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

    def remove_old_rows(self, state, duration, *args, **kwargs):
        state['rows'] = {k: v for (k, v) in state['rows'].items()
                         if k >= duration}
        return state

    def get_total_requests(self, *args, **kwargs):
        total_requests = 0
        for event_time in self.state['rows']:
            for section in self.state['rows'][event_time]:
                total_requests += self.state['rows'][event_time][section]
        return total_requests

    def parse_line(self, line, *args, **kwargs):
        log.debug('line: %s', line)

        delimiter = kwargs.get('delimiter', ',')
        quotechar = kwargs.get('quotechar', '"')
        timestamp_column = kwargs.get('timestamp_column', 3)
        section_column = kwargs.get('section_column', 4)

        reader = csv.reader([line], delimiter=delimiter, quotechar=quotechar)
        row = next(reader)

        timestamp = self.get_timestamp(row, timestamp_column)
        event_time = self.get_event_time(timestamp)
        stats_begin_datetime = event_time - \
            timedelta(seconds=self.stats_seconds)
        alert_begin_datetime = event_time - \
            timedelta(seconds=self.traffic_alert_minutes * 60)
        section = self.get_section(row, section_column)
        self.state = self.update_state(self.state, event_time, section)
        self.state = self.remove_old_rows(self.state, alert_begin_datetime)

        # Whenever total traffic for the past 2 minutes exceeds a certain number on
        # average, print a message to the console saying that “High traffic
        # generated an alert - hits = {value}, triggered at {time}”. The default
        # threshold should be 10 requests per second but should be configurable.
        total_requests = self.get_total_requests()

        # “High traffic generated an alert - hits = {value}, triggered at
        # {time}”. The default threshold should be 10 requests per second but
        # should be configurable.
        if ((total_requests > self.traffic_alert_minutes * 60 *
                self.traffic_alert_requests_per_minute) and not self.state['stats']['is_traffic_alerting']):
            self.state['stats']['is_traffic_alerting'] = True
            log.info('High traffic generated an alert - hits = %s, triggered at %s',
                     total_requests, event_time)
        elif ((total_requests <= self.traffic_alert_minutes * 60 *
                self.traffic_alert_requests_per_minute) and self.state['stats']['is_traffic_alerting']):
            self.state['stats']['is_traffic_alerting'] = False
            log.info('High traffic alert recovered - hits = %s, triggered at %s',
                     total_requests, event_time)

        # stats_rows = {
        #     k: v for (k, v) in self.state['rows'].items()
        #     if k >= stats_begin_datetime
        # }

        # pp.pprint('stats state: {}'.format(stats_rows))

        # For every 10 seconds of log lines, display stats about the traffic
        # during those 10 seconds: the sections of the web site with the most hits

        return self.state

    def get_input(self, *args, **kwargs):
        if self.file is None:
            return sys.stdin
        return open(self.file, 'r')

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

        # TODO: throwaway header
        with self.get_input() as file:
            for line in file:
                try:
                    self.parse_line(line, None)
                # pylint: disable=broad-except
                except Exception as err:
                    log.error('err: %s', err)

        pp.pprint(self.state)
