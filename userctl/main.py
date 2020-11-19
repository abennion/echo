# pylint: disable=C0103,C0111
from __future__ import print_function
import os
from fabric.main import Fab
from fabric.config import Config
from .executor import FabExecutor
from . import __version__ as version


class UserCtl(Fab):
    def load_collection(self):
        # unless set by the user, update the search root to within our
        # package module
        if self.args['search-root'].value is None:
            path = os.path.dirname(os.path.abspath(__file__))
            print("path: {}".format(path))
            self.args['search-root'].value = path
        super(UserCtl, self).load_collection()


program = UserCtl(
    name="userctl",
    version=version,
    executor_class=FabExecutor,
    config_class=Config
)
