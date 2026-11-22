CREATE DATABASE "Magazin_Smartphones";
CREATE USER eugen WITH PASSWORD 'eug3n&D1ana!';

ALTER ROLE eugen SET client_encoding TO 'utf8';
ALTER ROLE eugen SET default_transaction_isolation TO 'read committed';
ALTER ROLE eugen SET timezone TO 'Europe/Bucharest';

GRANT ALL PRIVILEGES ON DATABASE "Magazin_Smartphones" TO eugen;

\c "Magazin_Smartphones"
CREATE SCHEMA IF NOT EXISTS django AUTHORIZATION eugen;
GRANT ALL ON SCHEMA django TO eugen;