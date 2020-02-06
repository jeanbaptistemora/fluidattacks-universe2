#!/bin/bash

set -o errexit

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

# Create user
execute_query "
CREATE LOGIN $DB_USER WITH PASSWORD = \"$DB_PASSWORD\";
USE $DB_NAME;
CREATE USER $DB_USER FOR LOGIN $DB_USER WITH DEFAULT_SCHEMA = $DB_NAME;
GO"

# Enabled xp_cmdshell. check: can_execute_commands
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

# Enable ad hoc distributed queries check: has_enabled_ad_hoc_queries
execute_query "
sp_configure 'show advanced options', 1;
RECONFIGURE;
GO
sp_configure 'Ad Hoc Distributed Queries', 1;
RECONFIGURE;
GO

SELECT a.*
FROM OPENROWSET('SQLNCLI', 'Server=Seattle1;Trusted_Connection=yes;',
     'SELECT GroupName, Name, DepartmentID
      FROM AdventureWorks2012.HumanResources.Department
      ORDER BY GroupName, Name') AS a;
GO
"

# Enable agent xps option
execute_query "
sp_configure 'show advanced options', 1;
GO
RECONFIGURE WITH OVERRIDE;
GO
sp_configure 'Agent XPs', 1;
GO
RECONFIGURE WITH OVERRIDE
GO"

# Enable TRUSTWORTHY
execute_query "
ALTER DATABSE $DB_NAME SET TRUSTWORTHY ON"

# Grant permission ALTER ANY DATABASE. check: can_alter_any_database
execute_query "
GRANT ALTER ANY DATABASE TO $DB_USER;"

# Disablde password check policy
execute_query "
ALTER LOGIN $DB_USER WITH check_policy = OFF"
