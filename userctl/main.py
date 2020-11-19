# pylint: disable=C0103,C0111
from __future__ import print_function
import os
import logging
# from fabric.main import Fab
# from fabric.config import Config
# from .executor import FabExecutor
from invoke import Program
from . import __version__ as version

# TODO: pass in config from args
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        # rotating file handler
        logging.StreamHandler()  # sys.stdout
    ]
)

# class UserCtl(Fab):
#     def load_collection(self):
#         # unless set by the user, update the search root to within our
#         # package module
#         if self.args['search-root'].value is None:
#             path = os.path.dirname(os.path.abspath(__file__))
#             print("path: {}".format(path))
#             self.args['search-root'].value = path
#         super(UserCtl, self).load_collection()


# program = UserCtl(
#     name="userctl",
#     version=version,
#     executor_class=FabExecutor,
#     config_class=Config
# )

class UserCtl(Program):
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
    version=version
    # executor_class=FabExecutor,
    # config_class=Config
)
