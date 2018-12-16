#!/bin/sh

psql -f dropandcreatedb.sql
psql -d taskmaster -f dbsetup.sql
