# pylint: disable=W0613,C0111
"""
User managers implemented for different host environments.
"""
from userctl.utils import load_platform_subclass


class Users(object):
    """
    User manager for a generic Linux host.
    """

    PASSWD_USERNAME = 0
    PASSWD_PASSWORD = 1
    PASSWD_UID = 2
    PASSWD_GID = 3
    PASSWD_COMMENT = 4
    PASSWD_HOME = 5
    PASSWD_SHELL = 6

    platform = 'Linux'
    distribution = None
    runner = None

    def __new__(cls, *args, **kwargs):
        """
        Returns a subclass matching the platform and distribution.
        """
        return load_platform_subclass(Users, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.post_initialize(*args, **kwargs)

    def post_initialize(self, *args, **kwargs):
        self.runner = kwargs.get('runner', None)

    def run_command(self, cmd, *args, **kwargs):
        return self.runner.run_command(cmd, *args, **kwargs)

    def dir_exists(self, dirname, **kwargs):
        """
        Returns True if the directory exists.
        """
        cmd = '[ ! -d "{}" ] || echo "1"'.format(dirname)
        text = self.run_command(cmd, **kwargs)
        return text.strip() == "1"

    def create_user_useradd(self, name, **kwargs):
        """
        Creates a user via useradd.
        """
        # TODO check if the user already exists
        cmd = "useradd -m -d /home/{0} -s /bin/bash {0}".format(name)
        return self.run_command(cmd, **kwargs)

    def list_users_passwd(self, **kwargs):
        """
        Returns a dict of user passwd information.
        """
        cmd = "getent passwd"
        text = self.run_command(cmd, **kwargs)
        users = {}
        for line in text.strip().split('\n'):
            parts = line.split(':')
            if '/home' in parts[self.PASSWD_HOME]:
                # this doesn't really need to be a dict
                users[parts[self.PASSWD_USERNAME]] = {
                    'uid': parts[self.PASSWD_UID],
                    'comment': parts[self.PASSWD_COMMENT],
                    'home': parts[self.PASSWD_HOME]
                }
        return users

    def delete_user_userdel(self, name, **kwargs):
        """
        Deletes a user via userdel.
        """
        cmd = "userdel -f -r {}".format(name)
        return self.run_command(cmd, **kwargs)

    def make_dir(self, dirname, **kwargs):
        """
        Makes a new directory.
        """
        cmd = "mkdir -p {}".format(dirname)
        self.run_command(cmd, **kwargs)

    @classmethod
    def ssh_dirname(cls, name):
        return "/home/{}/.ssh".format(name)

    def make_sshdir(self, name, **kwargs):
        """
        Creates a user .ssh directory.
        """
        dirname = self.ssh_dirname(name)
        if not self.dir_exists(dirname, **kwargs):
            self.make_dir(dirname, **kwargs)
        cmd = "chown -R {0}:{0} {1}".format(name, dirname)
        self.run_command(cmd, **kwargs)
        cmd = "chmod 700 {}".format(dirname)
        self.run_command(cmd, **kwargs)

    @classmethod
    def authorized_keys_filename(cls, name):
        return "/home/{}/.ssh/authorized_keys".format(name)

    def make_authorized_keys(self, name, **kwargs):
        """
        Makes the authorized_keys file.
        """
        filename = self.authorized_keys_filename(name)
        cmd = "touch {}".format(filename)
        self.run_command(cmd, **kwargs)
        cmd = "chown -R {0}:{0} {1}".format(name, filename)
        self.run_command(cmd, **kwargs)
        cmd = "chmod 600 {}".format(filename)
        self.run_command(cmd, **kwargs)

    def get_authorized_keys(self, name, **kwargs):
        filename = self.authorized_keys_filename(name)
        cmd = "cat {}".format(filename)
        return self.run_command(cmd, **kwargs).strip()

    def set_authorized_key(self, name, public_key, **kwargs):
        """
        Set an authorized key.
        """
        filename = self.authorized_keys_filename(name)
        authorized_keys = self.get_authorized_keys(name, **kwargs)
        if not public_key in authorized_keys:
            cmd = "bash -c \"echo '{0}' >> {1}\"".format(public_key, filename)
            self.run_command(cmd, **kwargs)

    def create_user(self, name, public_key, **kwargs):
        """
        Creates a new user and adds an authorized key.
        """
        self.create_user_useradd(name, **kwargs)
        cmd = "usermod --lock {}".format(name)
        self.run_command(cmd, **kwargs)
        self.make_sshdir(name, **kwargs)
        self.make_authorized_keys(name, **kwargs)
        self.set_authorized_key(name, public_key, **kwargs)

    def list_users(self, **kwargs):
        """
        Lists users with a home directory.
        """
        users = self.list_users_passwd(**kwargs)
        res = ""
        for username, details in users.items():
            res += "username: {}, uid: {}, comment: {}\n".format(
                username, details['uid'], details['comment'])
        return res.strip()

    def delete_user(self, name, **kwargs):
        """
        Deletes a user.
        """
        self.delete_user_userdel(name, **kwargs)


class CentOsUsers(Users):
    """
    Demonstrates a platform specific subclass.
    """

    platform = 'Linux'
    distribution = "Centos linux"

    def list_users(self, **kwargs):
        users = self.list_users_passwd(**kwargs)
        res = "NOTE: using the centos users subclass\n"
        for username, details in users.items():
            res += "username: {}, uid: {}, comment: {}\n".format(
                username, details['uid'], details['comment'])
        return res.strip()
