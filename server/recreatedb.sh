#!/bin/sh

# Sending stdout to /dev/null gets rid of success messages,
# leaving error (and notice) messages to get displayed.
echo Drop and recreate database.
su postgres -c "psql -f dropandcreatedb.sql" || exit 1
echo Create schema.
su nate -c "psql -d taskmaster -f dbsetup.sql" >/dev/null

