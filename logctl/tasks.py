# pylint: disable=C0103,W0613,C0111
"""
Tasks for managing log files.
"""
from __future__ import print_function
import logging as log
from invoke import task
from logctl.runners import create_instance as create_runner
from logctl.log_parser import LogParser


@task
def parse_log(ctx, file=None):
    """
    Parse log by file name or stdin.
    """
    runner = create_runner('invoke', connection=ctx)
    parser = LogParser(runner=runner, file=file)
    parser.parse()
    log.info('done')
