GRANT USAGE ON SCHEMA "repos-s3-sync" TO repo_sync_user
GRANT SELECT, INSERT ON TABLE "repos-s3-sync".last_sync_date TO repo_sync_user
GRANT UPDATE (sync_date) ON TABLE "repos-s3-sync".last_sync_date TO repo_sync_user
