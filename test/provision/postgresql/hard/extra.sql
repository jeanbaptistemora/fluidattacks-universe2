/* does_not_support_ssl */

ALTER SYSTEM SET ssl TO 'on';
ALTER SYSTEM SET ssl_key_file TO '/var/lib/postgresql/server.key';
ALTER SYSTEM SET ssl_cert_file TO '/var/lib/postgresql/server.crt';

/* has_not_loggin_enabled */

ALTER SYSTEM SET logging_collector TO 'on';
ALTER SYSTEM SET log_statement TO 'all';
ALTER SYSTEM SET log_directory TO 'log';
ALTER SYSTEM SET log_filename TO 'postgresql-%Y-%m-%d_%H%M%S.log';

/* store_passwords_insecurely */

ALTER SYSTEM SET password_encryption TO 'scram-sha-256';
