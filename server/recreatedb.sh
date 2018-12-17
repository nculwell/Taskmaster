#!/bin/sh

su postgres -c "psql -f dropandcreatedb.sql"
su nate -c "psql -d taskmaster -f dbsetup.sql"

