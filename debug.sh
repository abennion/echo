#!/usr/bin/env bash

logctl parse-log -f ./docs/echo-coding-challenge-logs.csv

# echo '"remotehost","rfc931","authuser","date","request","status","bytes"
# "10.0.0.2","-","apache",1549573860,"GET /api/user HTTP/1.0",200,1234
# "10.0.0.4","-","apache",1549573860,"GET /api/user HTTP/1.0",200,1234
# "10.0.0.4","-","apache",1549573860,"GET /api/user HTTP/1.0",200,1234
# "10.0.0.2","-","apache",1549573860,"GET /api/help HTTP/1.0",200,1234
# "10.0.0.5","-","apache",1549573860,"GET /api/help HTTP/1.0",200,1234
# "10.0.0.4","-","apache",1549573859,"GET /api/help HTTP/1.0",200,1234
# "10.0.0.5","-","apache",1549573860,"POST /report HTTP/1.0",500,1307
# "10.0.0.3","-","apache",1549573860,"POST /report HTTP/1.0",200,1234
# "10.0.0.3","-","apache",1549573860,"GET /report HTTP/1.0",200,1194
# "10.0.0.4","-","apache",1549573861,"GET /api/user HTTP/1.0",200,1136
# "10.0.0.5","-","apache",1549573861,"GET /api/user HTTP/1.0",200,1194
# "10.0.0.1","-","apache",1549573861,"GET /api/user HTTP/1.0",200,1261
# "10.0.0.3","-","apache",1549573860,"GET /api/help HTTP/1.0",200,1234
# "10.0.0.2","-","apache",1549573861,"GET /api/help HTTP/1.0",200,1194
# "10.0.0.5","-","apache",1549573860,"GET /api/help HTTP/1.0",200,1234
# "10.0.0.2","-","apache",1549573861,"GET /report HTTP/1.0",200,1136
# "10.0.0.5","-","apache",1549573861,"POST /report HTTP/1.0",200,1136
# "10.0.0.5","-","apache",1549573862,"GET /report HTTP/1.0",200,1261
# "10.0.0.2","-","apache",1549573863,"POST /api/user HTTP/1.0",404,1307
# "10.0.0.2","-","apache",1549573862,"GET /api/user HTTP/1.0",200,1234
# "10.0.0.4","-","apache",1549573861,"GET /api/user HTTP/1.0",200,1234
# "10.0.0.1","-","apache",1549573862,"GET /api/help HTTP/1.0",500,1136
# "10.0.0.4","-","apache",1549573862,"POST /api/help HTTP/1.0",200,1234
# "10.0.0.1","-","apache",1549573862,"GET /api/help HTTP/1.0",200,1234
# "10.0.0.1","-","apache",1549573862,"GET /report HTTP/1.0",500,1194
# "10.0.0.2","-","apache",1549573862,"GET /report HTTP/1.0",200,1307
# "10.0.0.2","-","apache",1549573863,"GET /report HTTP/1.0",200,1194' | logctl parse-log
