#!/bin/bash

set -o errexit

execute_query () {
    /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P $SA_PASSWORD -Q "$1"
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
INSERT INTO users VALUES ('user1', 'c878cba33f53e16643c1679d831075e0');
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

# Set exiration password. check: has_login_password_expiration_disabled
execute_query "
ALTER LOGIN sa WITH CHECK_EXPIRATION = ON;
GO
ALTER LOGIN $DB_USER WITH CHECK_EXPIRATION = ON"

# Create asymmetric key.
# check: has_asymmetric_keys_with_unencrypted_private_keys
execute_query "
USE $DB_NAME;
GO
CREATE ASYMMETRIC KEY asserts_key
    WITH ALGORITHM = RSA_2048
    ENCRYPTION BY PASSWORD = '5M_~C67k,QNw\uzT';
GO
"

# Disbled SMO and DMO XPs option: check: has_smo_and_dmo_xps_option_enabled
execute_query "
EXEC sp_configure 'show advanced options', 1;
GO
RECONFIGURE;
GO
EXEC sp_configure 'SMO and DMO XPs', '0';
GO
RECONFIGURE;"

# Set autoclose ON. check: has_contained_dbs_with_auto_close_enabled
execute_query "
CREATE DATABASE test_db_1;
GO
EXEC sp_configure 'contained database authentication', 1
GO
RECONFIGURE;
GO
ALTER DATABASE test_db_1 SET containment = PARTIAL;
GO
ALTER DATABASE test_db_1 SET AUTO_CLOSE OFF;"

# Disbled remote access. check: has_remote_access_option_enabled
# Server must be restarted
execute_query "
EXEC sp_configure 'remote access', 0 ;
GO
RECONFIGURE;
GO"


# # Disable sa account. check: has_sa_account_login_enabled
# execute_query "ALTER LOGIN sa DISABLE;"

# Create storated procedure. check: has_unencrypted_storage_procedures
execute_query "
USE $DB_NAME
GO
CREATE PROCEDURE get_asymmetric_keys
    WITH ENCRYPTION
AS
BEGIN
    SELECT name, pvt_key_encryption_type
    FROM sys.asymmetric_keys
END"
