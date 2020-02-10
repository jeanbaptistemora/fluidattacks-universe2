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
