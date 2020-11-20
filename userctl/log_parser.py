# pylint: disable=W0613, C0111
"""
Parses logs, potentially for different host environments. Written for Frabric 
originally. It could be adapted for remote calls.
"""

import sys
import csv
import logging as log
from datetime import datetime, timedelta


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
        """
        Returns the initial state of the log summary.
        """
        return {
            'is_traffic_alerting': False,
            'stats_reported_on': None,
            'rows': {}
        }

    def get_section(self, row, col, *args, **kwargs):
        """
        Returns the log entry section.
        """
        # Not great, but it works.
        text = row[col]
        path = text.split(' ')[1]
        return path.split('/')[1]

    def get_timestamp(self, row, col, *args, **kwargs):
        """
        Returns the timestamp of the log entry.
        """
        return int(row[col])

    def get_event_date(self, timestamp, *args, **kwargs):
        """
        Returns the event datetime of the log entry based on the timestamp.
        """
        return datetime.fromtimestamp(timestamp)

    def update_state(self, state, event_date, section, *args, **kwargs):
        """
        Updates the state of the log summary.
        """
        # event_date / section: count
        if not event_date in state['rows'].keys():
            state['rows'][event_date] = {
                section: 1
            }
        else:
            if not section in state['rows'][event_date].keys():
                state['rows'][event_date][section] = 1
            else:
                state['rows'][event_date][section] += 1
        return state

    def remove_old_rows(self, state, from_datetime, *args, **kwargs):
        """
        Remove rows older than the specified datetime.
        """
        state['rows'] = {
            k: v for (k, v) in state['rows'].items() if k >= from_datetime
        }
        return state

    def get_total_requests(self, *args, **kwargs):
        """
        Returns the total summary count of requests.
        """
        total_requests = 0
        for event_date in self.state['rows']:
            for section in self.state['rows'][event_date]:
                total_requests += self.state['rows'][event_date][section]
        return total_requests

    def check_traffic(self, state, event_date, *args, **kwargs):
        # NOTE: Whenever total traffic for the past 2 minutes exceeds a certain
        # number on average, print a message to the console saying that “High
        # traffic generated an alert - hits = {value}, triggered at {time}”.
        # The default threshold should be 10 requests per second but should be
        # configurable.
        # TODO: but should be configurable
        total_requests = self.get_total_requests()
        if ((total_requests > self.traffic_alert_minutes * 60 *
                self.traffic_alert_requests_per_minute)
                and not state['is_traffic_alerting']):
            state['is_traffic_alerting'] = True
            msg = 'High traffic generated an alert - hits = {}, triggered at {}'
            print(msg.format(total_requests, event_date))
        elif ((total_requests <= self.traffic_alert_minutes * 60 *
                self.traffic_alert_requests_per_minute)
                and state['is_traffic_alerting']):
            state['is_traffic_alerting'] = False
            msg = 'High traffic alert recovered - hits = {}, triggered at {}'
            print(msg.format(total_requests, event_date))
        return state

    def check_stats(self, state, event_date, *args, **kwargs):
        # NOTE: For every 10 seconds of log lines, display stats about the traffic
        # during those 10 seconds: the sections of the web site with the most
        # hits.

        # if we haven't checked stats before, set a value and return state
        if state['stats_reported_on'] is None:
            state['stats_reported_on'] = event_date
            return state

        # print('test3')

        from_date = event_date - timedelta(
            seconds=self.stats_seconds)

        # print('test4', state['stats_reported_on'])

        # if event_date - stats_reported_on is less than 10 seconds, exit
        if state['stats_reported_on'] > from_date:
            # print('test5')
            return state

        # print('test6')

        # filter out rows older than the from date
        stats_rows = {
            k: v for (k, v) in state['rows'].items()
            if k >= from_date
        }

        # else, has it been 10 seconds? we need the new max datetime?

        stats = {}
        for value in stats_rows.values():
            for section, count in value.items():
                if not section in stats:
                    stats[section] = 0
                stats[section] += count

        print('stats', event_date, stats)

        state['stats_reported_on'] = event_date

        return state

    def get_row(self, line, *args, **kwargs):
        # TODO: Create factory to handle other types of logs.
        delimiter = kwargs.get('delimiter', ',')
        quotechar = kwargs.get('quotechar', '"')
        reader = csv.reader([line], delimiter=delimiter, quotechar=quotechar)
        return next(reader)

    def parse_line(self, line, *args, **kwargs):
        """
        Parse and handle the specified log line entry.
        """
        log.debug('line: %s', line)
        timestamp_column = kwargs.get('timestamp_column', 3)
        section_column = kwargs.get('section_column', 4)

        row = self.get_row(line, *args, **kwargs)
        timestamp = self.get_timestamp(row, timestamp_column)
        event_date = self.get_event_date(timestamp)
        section = self.get_section(row, section_column)

        self.state = self.update_state(self.state, event_date, section)

        alert_from_date = event_date - timedelta(
            seconds=self.traffic_alert_minutes * 60)

        self.state = self.remove_old_rows(self.state, alert_from_date)
        self.state = self.check_traffic(self.state, event_date)
        self.state = self.check_stats(self.state, event_date)

        return self.state

    def get_input(self, *args, **kwargs):
        if self.file is None:
            return sys.stdin
        return open(self.file, 'r')

    def parse(self, *args, **kwargs):
        # TODO: try in python2.7
        # TODO: unit tests
        self.state = LogParser.init_state()

        with self.get_input() as file:
            for line in file:
                try:
                    self.parse_line(line, None)
                # pylint: disable=broad-except
                except Exception as err:
                    log.error('err: %s', err)
