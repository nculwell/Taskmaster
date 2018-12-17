#!/bin/sh

PORT=8235

#twistd -n web --port tcp:$PORT --wsgi server.taskmaster
gunicorn3 -b 127.0.0.1:$PORT server.app
