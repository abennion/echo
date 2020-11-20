# pylint: disable=W0122,C0103,C0111
import os
import setuptools


package_name = "logctl"
binary_name = "logctl"

packages = setuptools.find_packages(
    include=["logctl", "{}.*".format("logctl")]
)

_locals = {}
with open(os.path.join(package_name, "_version.py")) as fp:
    exec(fp.read(), None, _locals)
version = _locals["__version__"]

setuptools.setup(
    name=package_name,
    version=version,
    description="User manager.",
    license="MIT",
    author="John Doe",
    author_email="jdoe@example.com",
    url="http://logctl.example.com",
    install_requires=[
        "invoke>=1.0,<2.0"
    ],
    packages=packages,
    entry_points={
        "console_scripts": [
            "{} = {}.main:program.run".format(binary_name, package_name)
        ]
    },
)
