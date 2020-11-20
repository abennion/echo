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
    def init_state():
        """
        Returns the initial state of the log summary.
        """
        return {
            'is_traffic_alerting': False,
            'stats_reported_on': None,
            'rows': {}
        }

    @staticmethod
    def get_section(row, col):
        """
        Returns the log entry section.
        """
        # Not great, but it works.
        text = row[col]
        path = text.split(' ')[1]
        return path.split('/')[1]

    @staticmethod
    def get_timestamp(row, col):
        """
        Returns the timestamp of the log entry.
        """
        return int(row[col])

    @staticmethod
    def get_event_date(timestamp):
        """
        Returns the event datetime of the log entry based on the timestamp.
        """
        return datetime.fromtimestamp(timestamp)

    @staticmethod
    def update_rows(rows, event_date, section):
        """
        Updates the log summary rows.
        """
        # event_date / section: count
        if not event_date in rows.keys():
            rows[event_date] = {
                section: 1
            }
        else:
            if not section in rows[event_date].keys():
                rows[event_date][section] = 1
            else:
                rows[event_date][section] += 1
        return rows

    @staticmethod
    def remove_old_rows(rows, event_date, traffic_alert_minutes):
        """
        Remove rows older than the specified datetime.
        """
        time_delta = timedelta(seconds=traffic_alert_minutes * 60)
        from_date = event_date - time_delta
        return {k: v for (k, v) in rows.items() if k >= from_date}

    @staticmethod
    def get_total_requests(rows):
        """
        Returns the total summary count of requests.
        """
        total_requests = 0
        for event_date in rows:
            for section in rows[event_date]:
                total_requests += rows[event_date][section]
        return total_requests

    def check_traffic(self, state, event_date):
        """
        Prints an alert when total traffic exceeds a threshold over a specified
        period of time.
        """
        total_requests = LogParser.get_total_requests(self.state['rows'])
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

    def check_stats(self, state, event_date):
        """
        Prints summary statistics for the last 10 seconds of log entries based
        on event time. The summary is an approximation since log messages may
        not be received in order.
        """
        if state['stats_reported_on'] is None:
            state['stats_reported_on'] = event_date
            return state

        # TODO: pass in as an argument
        from_date = event_date - timedelta(seconds=self.stats_seconds)

        if from_date <= state['stats_reported_on']:
            return state

        # Filter rows older than the summary interval.
        rows = {
            k: v for (k, v) in state['rows'].items()
            if k >= from_date
        }

        # Summarize count of requests by event date and section.
        stats = {}
        for value in rows.values():
            for section, count in value.items():
                if not section in stats:
                    stats[section] = 0
                stats[section] += count

        state['stats_reported_on'] = event_date

        # TODO: Make prettier.
        print('{}: {}'.format(event_date, stats))
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
        # log.debug('line: %s', line)
        timestamp_column = kwargs.get('timestamp_column', 3)
        section_column = kwargs.get('section_column', 4)

        row = self.get_row(line, *args, **kwargs)

        timestamp = self.get_timestamp(row, timestamp_column)
        event_date = self.get_event_date(timestamp)
        section = self.get_section(row, section_column)

        self.state['rows'] = LogParser.update_rows(
            self.state['rows'], event_date, section)

        self.state['rows'] = LogParser.remove_old_rows(
            self.state['rows'],
            event_date,
            self.traffic_alert_minutes
        )

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
