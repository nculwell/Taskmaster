#!/bin/sh


PORT=8257

USR=njc
PWD=xxx
URL=http://localhost:$PORT

CJ=cookiejar.txt

req() {
  echo "$@"
  curl -b "$CJ" -c "$CJ" "$@"
}

echo login
req -j -F "usr=$USR" -F "pwd=$PWD" "$URL/login"

echo task
req "$URL/task/1"

