# userctl

## Overview

Userctl is a sample user management CLI written in Python using the
[Fabric](https://github.com/fabric/fabric) library. Userctl lets you:

* Add, list, or delete users on a remote host

A second solution is provided as an [Ansible](https://www.ansible.com/)
playbook. The code and documentation are [here](ansible).

Update: The code has been implemented and tested with handlers for Ubuntu and
CentOS to demonstrate extensibility. I have not extended support to other
Unix-like platforms or Windows.

Both Fabric and Ansible use the
[Paramiko](https://github.com/paramiko/paramiko) SSH library.

## Prerequisites

The user should be configured with sufficient permissions to execute commands
using sudo on the remote host via SSH.

## Installation

```bash
git clone https://github.com/abennion/userctl.git
# create python virtual environment and install the component locally
make setup && make install
source venv/bin/activate
```

Or from PIP:

```bash
pip install -e git+https://github.com/abennion/userctl#egg=userctl
```

## Usage

```bash
# show the core arguments
# NOTE: not all core Fab arguments are supported at this time
userctl --help

# list users
userctl --help list-users
userctl -H foo.example.com,bar.example.com list-users

# add a user
userctl --help add-user
# Options:
#   -p STRING, --public-key-filename=STRING
#   -u STRING, --user=STRING
userctl -H foo.example.com,bar.example.com add-user \
    -u johndoe -p ~/.ssh/johndoe/id_rsa.pub

# delete a user
userctl --help delete-user
# Options:
#   -u STRING, --user=STRING
userctl -H foo.example.com,bar.example.com delete-user -u johndoe
```