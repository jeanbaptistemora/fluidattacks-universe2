
/* has_insecure_file_permissions */

ALTER SYSTEM SET log_file_mode TO '0666';

/* allows_too_many_concurrent_connections */

ALTER SYSTEM SET max_connections TO '1000';
