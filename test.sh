#!/bin/sh


PORT=8257

USR=njc
PWD=xxx
URL=http://localhost:$PORT

CJ=cookiejar.txt

req() {
  echo "$@"
  curl -b "$CJ" -c "$CJ" "$@"
  echo
}

echo login
req -j -F "usr=$USR" -F "pwd=$PWD" "$URL/login"
echo task
req "$URL/task/1"
echo user
req "$URL/user/1"
echo user tasks
req "$URL/task/user/1"
echo bad service
req "$URL/badservice"
echo bad user
req "$URL/user/99"

