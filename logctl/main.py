# pylint: disable=C0103,C0111
from __future__ import print_function
import os
import sys
import logging
from invoke import Program
from . import __version__ as version

# TODO: make configurable
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


class logctl(Program):
    def load_collection(self):
        # Unless specified by the user, search within the module.
        if self.args['search-root'].value is None:
            path = os.path.dirname(os.path.abspath(__file__))
            print("path: {}".format(path))
            self.args['search-root'].value = path
        super(logctl, self).load_collection()


program = logctl(
    name="logctl",
    version=version
)
