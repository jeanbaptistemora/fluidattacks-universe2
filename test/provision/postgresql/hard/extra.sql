/* does_not_support_ssl */

ALTER SYSTEM SET ssl TO 'on';
ALTER SYSTEM SET ssl_key_file TO '/var/lib/postgresql/server.key';
ALTER SYSTEM SET ssl_cert_file TO '/var/lib/postgresql/server.crt';

/* has_not_loggin_enabled */

ALTER SYSTEM SET logging_collector TO 'on';
ALTER SYSTEM SET log_statement TO 'all';
ALTER SYSTEM SET log_filename TO 'postgresql-%Y-%m-%d_%H%M%S.log';
ALTER SYSTEM SET log_directory TO 'log';

ALTER SYSTEM SET log_line_prefix TO '%m %c %u@%d[%r]';

ALTER SYSTEM SET log_destination TO 'stderr';
ALTER SYSTEM SET log_truncate_on_rotation TO 'off';

ALTER SYSTEM SET log_lock_waits TO 'on';
ALTER SYSTEM SET log_checkpoints TO 'on';
ALTER SYSTEM SET log_connections TO 'on';
ALTER SYSTEM SET log_disconnections TO 'on';
ALTER SYSTEM SET log_replication_commands TO 'on';

ALTER SYSTEM SET log_autovacuum_min_duration TO '0';
ALTER SYSTEM SET log_min_duration_statement TO '0';

ALTER SYSTEM SET log_min_messages TO 'warning';
ALTER SYSTEM SET log_error_verbosity TO 'verbose';
ALTER SYSTEM SET log_min_error_statement TO 'error';

ALTER SYSTEM SET log_duration TO 'on';
ALTER SYSTEM SET log_statement_stats TO 'off';
ALTER SYSTEM SET log_executor_stats TO 'on';
ALTER SYSTEM SET log_parser_stats TO 'on';
ALTER SYSTEM SET log_planner_stats TO 'on';

/* store_passwords_insecurely */

ALTER SYSTEM SET password_encryption TO 'scram-sha-256';

/* allows_too_many_concurrent_connections */

ALTER SYSTEM SET max_connections TO '100';
