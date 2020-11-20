# logctl

## Overview

A simple HTTP log parser written with Invoke.

## Installation

```bash
git clone https://github.com/abennion/echo.git
# create python virtual environment and install the component locally
make setup
source ./venv/bin/activate
make install
```

Or from PIP:

```bash
pip install -e git+https://github.com/abennion/echo#egg=logctl
```

## Usage

```bash
# show the core arguments
logctl --help

# parse-log
logctl parse-log -f ./docs/echo-coding-challenge-logs.csv

# pipe data through stdin
echo '"remotehost","rfc931","authuser","date","request","status","bytes"
"10.0.0.2","-","apache",1549573860,"GET /api/user HTTP/1.0",200,1234
"10.0.0.4","-","apache",1549573860,"GET /api/user HTTP/1.0",200,1234
"10.0.0.2","-","apache",1549573862,"GET /report HTTP/1.0",200,1307
"10.0.0.2","-","apache",1549573863,"GET /report HTTP/1.0",200,1194' | logctl parse-log
```

## Notes

I only have a few brief notes at this time.

- This CLI is built around the Invoke task runner (pyinvoke)
- I did not have time to create unit tests using unittest or pytest
- There are likely numerous bugs
- I have not tried running it against Python2.7, but it should work with minor
  adjustments
- Performance is likely not optimal. I chose to use a Dictionary object as the
  main data structure. I'm sure that can be improved on
