-- Create roles for DS and MLE users
CREATE ROLE ds_user_role;
CREATE ROLE mle_user_role;

-- Grant permissions to roles
-- DS user gets read-only access
GRANT USAGE ON SCHEMA public TO ds_user_role;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ds_user_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO ds_user_role;

-- MLE user gets all permissions on public schema
GRANT ALL PRIVILEGES ON SCHEMA public TO mle_user_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mle_user_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO mle_user_role;

-- Create users with passwords
CREATE USER ds_user WITH PASSWORD 'ds_user';
CREATE USER mle_user WITH PASSWORD 'mle_user';

-- Assign roles to users
GRANT ds_user_role TO ds_user;
GRANT mle_user_role TO mle_user; 