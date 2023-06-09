#!/bin/bash

set -o errexit

execute_query() {
  /opt/mssql-tools/bin/sqlcmd -S tcp:localhost,1432 -U SA -P "${SA_PASSWORD}" -Q "$1"
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
GO"

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
GO"

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
GO"

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

# Grant permission ALTER ANY DATABASE. check: can_alter_any_database
execute_query "GRANT ALTER ANY DATABASE TO $DB_USER;"

# Disable password check policy. check: has_password_policy_check_disabled
execute_query "ALTER LOGIN $DB_USER WITH check_policy = OFF"

# Enable Agent XPs option. check: has_xps_option_enabled
execute_query "
EXEC sp_configure 'show advanced options', 1;
EXEC sp_configure 'Agent XPs', '1';
RECONFIGURE WITH OVERRIDE"

# Create asymmetric key.
# check: has_asymmetric_keys_with_unencrypted_private_keys
execute_query "
USE $DB_NAME;
GO
CREATE ASYMMETRIC KEY asserts_key
    WITH ALGORITHM = RSA_2048
    ENCRYPTION BY PASSWORD = '5M_~C67k,QNw\uzT';
GO
ALTER ASYMMETRIC KEY asserts_key REMOVE PRIVATE KEY;
GO"

# Set autoclose ON. check: has_contained_dbs_with_auto_close_enabled
execute_query "
CREATE DATABASE test_db_1;
GO
EXEC sp_configure 'contained database authentication', 1
GO
RECONFIGURE;
GO
ALTER DATABASE test_db_1 SET containment  = PARTIAL
GO
ALTER DATABASE test_db_1 SET AUTO_CLOSE ON"

# Enable TRUSTWORTHY. check: has_trustworthy_status_on
# Server must be restarted
execute_query "ALTER DATABSE test_db_1 SET TRUSTWORTHY ON"

# Grant Alter any login. check: can_alter_any_login
execute_query "GRANT ALTER ANY LOGIN TO $DB_USER"

# Grant Control Server check: can_alter_any_login
execute_query "GRANT CONTROL SERVER TO $DB_USER"

# Grant Control Server check: can_alter_any_login
execute_query "GRANT ALTER ANY CREDENTIAL TO $DB_USER"

# Create storated procedure. check: has_unencrypted_storage_procedures
execute_query "
USE $DB_NAME
GO
CREATE PROCEDURE get_asymmetric_keys
AS
BEGIN
    SELECT name, pvt_key_encryption_type
    FROM sys.asymmetric_keys
END"

# Grant permission SHUTDOWN. check: can_shutdown_server
execute_query "GRANT SHUTDOWN TO $DB_USER;"

# Enable clr enabled. check: has_clr_option_enabled
execute_query "
sp_configure 'clr enabled', 1;
GO
RECONFIGURE WITH OVERRIDE;
GO"
