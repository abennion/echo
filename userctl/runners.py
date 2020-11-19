# pylint: disable=W0613,C0111
"""
Runners for executing shell commands.
"""


def create_instance(name, *args, **kwargs):
    """
    Runner factory method.
    """
    classes = {
        'fabric': FabricRunner,
        'invoke': InvokeRunner
    }
    runner_class = None
    if name.lower() == 'fabric':
        runner_class = classes.get('fabric', FabricRunner)
    else:
        runner_class = classes.get('invoke', InvokeRunner)
    if runner_class:
        return runner_class(*args, **kwargs)
    raise NotImplementedError()


class RunnerBase(object):
    def __init__(self, *args, **kwargs):
        self.post_initialize(*args, **kwargs)

    def post_initialize(self, *args, **kwargs):
        pass

    def run_command(self, cmd, *args, **kwargs):
        raise NotImplementedError()


class FabricRunner(RunnerBase):
    """
    Command runner implemented using Fabric.
    """
    connection = None

    def post_initialize(self, *args, **kwargs):
        self.connection = kwargs.get('connection', None)

    def run_command(self, cmd, *args, **kwargs):
        fabric_kwargs = kwargs.get('fabric_kwargs', {})
        return self.connection.sudo(cmd, **fabric_kwargs).stdout


class InvokeRunner(RunnerBase):
    """
    Command runner implemented using Invoke.
    """
    connection = None

    def post_initialize(self, *args, **kwargs):
        self.connection = kwargs.get('connection', None)

    def run_command(self, cmd, *args, **kwargs):
        invoke_kwargs = kwargs.get('invoke_kwargs', {})
        return self.connection.run(cmd, **invoke_kwargs).stdout

    # def read_stdin(self, *args, **kwargs):
    #     return self.connection.read_our_stdin(sys.stdin)
