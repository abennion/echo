# pylint: disable=C0103,C0111
from __future__ import print_function
import os
import sys
import logging
from invoke import Program
from . import __version__ as version

logging.basicConfig(
    level=logging.INFO,  # DEBUG
    # format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)  # sys.stdout
    ]
)


class UserCtl(Program):
    def load_collection(self):
        # Unless specified by the user, search within the module.
        if self.args['search-root'].value is None:
            path = os.path.dirname(os.path.abspath(__file__))
            print("path: {}".format(path))
            self.args['search-root'].value = path
        super(UserCtl, self).load_collection()


program = UserCtl(
    name="userctl",
    version=version
)
