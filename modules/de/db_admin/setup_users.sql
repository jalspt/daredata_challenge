-- Setup users, roles and permissions for the PostgreSQL database
-- This script runs when the database container initializes

-- Create roles
CREATE ROLE ds_user_role;
CREATE ROLE mle_user_role;

-- Create users with passwords
CREATE USER ds_user WITH PASSWORD 'ds_user';
CREATE USER mle_user WITH PASSWORD 'mle_user';

-- Assign roles to users
GRANT ds_user_role TO ds_user;
GRANT mle_user_role TO mle_user;

-- Grant permissions to roles
-- DS user gets read-only access
GRANT USAGE ON SCHEMA public TO ds_user_role;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ds_user_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO ds_user_role;

-- MLE user gets all permissions on public schema
GRANT ALL PRIVILEGES ON SCHEMA public TO mle_user_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mle_user_role;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO mle_user_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO mle_user_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO mle_user_role;

-- Allow DS and MLE users to connect to the database
GRANT CONNECT ON DATABASE companydata TO ds_user;
GRANT CONNECT ON DATABASE companydata TO mle_user;

-- Make permissions apply to future objects
ALTER DEFAULT PRIVILEGES FOR ROLE admin IN SCHEMA public
GRANT SELECT ON TABLES TO ds_user_role;

ALTER DEFAULT PRIVILEGES FOR ROLE admin IN SCHEMA public
GRANT ALL PRIVILEGES ON TABLES TO mle_user_role;

-- Create initial tables with proper permissions
CREATE TABLE IF NOT EXISTS customer_profiles (
    idx INTEGER PRIMARY KEY,
    attr_a INTEGER,
    attr_b VARCHAR(1),
    attr_c VARCHAR(5)
);

CREATE TABLE IF NOT EXISTS customer_activity (
    idx INTEGER,
    valid_from DATE,
    valid_to DATE,
    scd_a NUMERIC,
    scd_b INTEGER,
    PRIMARY KEY (idx, valid_from)
);

CREATE TABLE IF NOT EXISTS labels (
    idx INTEGER PRIMARY KEY,
    label INTEGER
);

CREATE TABLE IF NOT EXISTS stores (
    idx INTEGER PRIMARY KEY,
    location VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS sales (
    idx INTEGER,
    value NUMERIC,
    date DATE,
    store_idx INTEGER,
    PRIMARY KEY (idx, date)
);

CREATE TABLE IF NOT EXISTS monthly_sales (
    store_idx INTEGER,
    location VARCHAR(50),
    sale_month DATE,
    value NUMERIC,
    PRIMARY KEY (store_idx, sale_month)
);

CREATE TABLE IF NOT EXISTS feature_store (
    idx INTEGER PRIMARY KEY,
    attr_a INTEGER,
    attr_b VARCHAR(1),
    scd_a NUMERIC,
    scd_b INTEGER,
    label INTEGER
);

-- Grant permissions on these tables
GRANT SELECT ON ALL TABLES IN SCHEMA public TO ds_user_role;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO mle_user_role; 