# Demo Dataset Schema

FrostSight ships with deterministic CSVs that emulate Snowflake ACCOUNT_USAGE views.

## warehouses.csv
- `name`: warehouse name
- `size`: size tier
- `credit_per_hour`: credit rate

## warehouse_metering.csv
- `warehouse_name`
- `start_time`
- `end_time`
- `credits_used`

## query_history.csv
- `query_id`
- `warehouse_name`
- `user_name`
- `role_name`
- `start_time`
- `end_time`
- `total_elapsed_ms`
- `bytes_scanned`
- `rows_produced`
- `query_text`

## role_grants.csv
- `role_name`
- `grantee_name`
- `grantee_type`
- `privilege`
- `granted_on`

## role_usage.csv
- `role_name`
- `last_used_at`

## object_access.csv
- `object_name`
- `object_type`
- `role_name`
- `access_count`
