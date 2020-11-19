# pylint: disable=C0111,W0613,C0103
from __future__ import print_function
from textwrap import dedent


def get_platform(*args, **kwargs):
    """
    Returns the platform of the remote host.
    """
    cmd = dedent("""\
        python - <<DOC
        from __future__ import print_function
        import platform
        print(platform.system())
        DOC
        """).strip()
    runner = kwargs.get('runner', None)
    return runner.run_command(cmd, *args, **kwargs).strip()


def get_distribution(*args, **kwargs):
    """
    Returns the distribution of the remote host.

    Source: https://github.com/ansible/ansible
    """
    cmd = dedent("""\
        python - <<DOC
        from __future__ import print_function
        import os
        import platform
        if platform.system() == 'Linux':
            try:
                supported_dists = platform._supported_dists + ('arch', 'alpine', 'devuan')
                distribution = platform.linux_distribution(supported_dists=supported_dists)[0].capitalize()
                if not distribution and os.path.isfile('/etc/system-release'):
                    distribution = platform.linux_distribution(supported_dists=['system'])[0].capitalize()
                    if 'Amazon' in distribution:
                        distribution = 'Amazon'
                    else:
                        distribution = 'OtherLinux'
            except:
                distribution = platform.dist()[0].capitalize()
        else:
            distribution = None
        print(distribution)
        DOC
        """).strip()
    runner = kwargs.get('runner', None)
    return runner.run_command(cmd, *args, **kwargs).strip()


def get_distribution_version(*args, **kwargs):
    """
    Returns the distribution version.

    Source: https://github.com/ansible/ansible
    """
    cmd = dedent("""\
        python - <<DOC
        from __future__ import print_function
        import os
        import platform
        if platform.system() == 'Linux':
            try:
                distribution_version = platform.linux_distribution()[1]
                if not distribution_version and os.path.isfile('/etc/system-release'):
                    distribution_version = platform.linux_distribution(supported_dists=['system'])[1]
            except:
                distribution_version = platform.dist()[1]
        else:
            distribution_version = None
        print(distribution_version)
        DOC
        """).strip()
    runner = kwargs.get('runner', None)
    return runner.run_command(cmd, *args, **kwargs).strip()


def get_all_subclasses(cls):
    """
    Returns all subclasses of a given class.

    Source: https://github.com/ansible/ansible
    """
    # Retrieve direct subclasses
    subclasses = cls.__subclasses__()
    to_visit = list(subclasses)
    # Then visit all subclasses
    while to_visit:
        for sc in to_visit:
            # The current class is now visited, so remove it from list
            to_visit.remove(sc)
            # Appending all subclasses to visit and keep a reference of available class
            for ssc in sc.__subclasses__():
                subclasses.append(ssc)
                to_visit.append(ssc)
    return subclasses


def load_platform_subclass(cls, *args, **kwargs):
    """
    Returns a platform specific subclass.

    Source: https://github.com/ansible/ansible
    """
    this_platform = get_platform(**kwargs)
    distribution = get_distribution(**kwargs)
    print("platform: {}, distribution: {}".format(
        this_platform, distribution))
    subclass = None

    # get the most specific superclass for this platform
    if distribution is not None:
        for sc in get_all_subclasses(cls):
            if (sc.distribution is not None and
                    sc.distribution == distribution and
                    sc.platform == this_platform):
                subclass = sc
    if subclass is None:
        for sc in get_all_subclasses(cls):
            if sc.platform == this_platform and sc.distribution is None:
                subclass = sc
    if subclass is None:
        subclass = cls

    return super(cls, subclass).__new__(subclass)
