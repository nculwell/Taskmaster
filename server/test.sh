#!/bin/sh


PORT=8257

USR=njc
PWD=xxx
URL=http://localhost:$PORT

curl -F "usr=$USR" -F "pwd=$PWD" $URL/login

