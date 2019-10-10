#!/bin/bash

execute_query () {
    /opt/mssql-tools/bin/sqlcmd -S tcp:localhost,1432 -U SA -P $SA_PASSWORD -Q "$1"
}

# create database
execute_query "
CREATE DATABASE $DB_NAME;
GO
USE $DB_NAME;
GO
CREATE TABLE users (
    name VARCHAR(16),
    password VARCHAR(16)
);
GO
INSERT INTO users VALUES ('user1', 'fluidasserts123.');
GO
select * from users;
GO
"

# create user
execute_query "
CREATE LOGIN $DB_USER WITH PASSWORD = \"$DB_PASSWORD\";
USE $DB_NAME;
CREATE USER $DB_USER FOR LOGIN $DB_USER WITH DEFAULT_SCHEMA = $DB_NAME;
GO"

# Enabled xp_cmdshell
execute_query "
-- To allow advanced options to be changed.
EXEC sp_configure 'show advanced options', 1;
GO
-- To update the currently configured value for advanced options.
RECONFIGURE;
GO
-- To enable the feature.
EXEC sp_configure 'xp_cmdshell', 1;
GO
-- To update the currently configured value for this feature.
RECONFIGURE;
GO
"
