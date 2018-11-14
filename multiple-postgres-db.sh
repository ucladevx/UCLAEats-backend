#!/bin/bash

# Bash script to set up multiple databases in Postgres
# Taken from https://github.com/mrts/docker-postgresql-multiple-databases/blob/master/create-multiple-postgresql-databases.sh
# Edited to use env var for the user

# Summary:
# Parameters:
# Env var $POSTGRES_MULTIPLE_DATABASES is the comma separated names of the DBs
# Env var $POSTGRES_USER and $POSTGRES_PASSWORD will be reused for all the DBs

# Detailed features used:
# Use psql to run postgres commands, postgres is the user with the auth
# needed in order to create users and dbs
# Use ON_ERROR_STOP to either crash or continue past errors

set -e
set -u

# function to create each database
function create_user_and_database() {
	local database=$1
	echo "  Creating user and database '$database'"
	psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
	    CREATE DATABASE $database;
	    GRANT ALL PRIVILEGES ON DATABASE $database TO $POSTGRES_USER;
EOSQL
}

# check if the env variable exists
if [ -n "$POSTGRES_MULTIPLE_DATABASES" ]; then
	echo "Multiple database creation requested: $POSTGRES_MULTIPLE_DATABASES"
	# ignore error in case user already exists
	psql -v ON_ERROR_STOP=0 --username postgres <<-EOSQL
		CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';
	EOSQL
	for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
		create_user_and_database $db
	done
	echo "Multiple databases created"
fi