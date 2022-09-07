-- SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
--
-- SPDX-License-Identifier: MPL-2.0

/* has_insecure_file_permissions */

ALTER SYSTEM SET log_file_mode TO '0666';

/* allows_too_many_concurrent_connections */

ALTER SYSTEM SET max_connections TO '1000';
