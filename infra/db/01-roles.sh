#!/bin/bash
# Roles con el mínimo privilegio necesario:
#   saapre_migrator: crea y modifica tablas (solo para migraciones).
#   saapre_app:      la API solo lee y escribe filas; no puede alterar el esquema.
set -euo pipefail

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE ROLE saapre_migrator LOGIN PASSWORD '${SAAPRE_MIGRATOR_PASSWORD}';
  CREATE ROLE saapre_app LOGIN PASSWORD '${SAAPRE_APP_PASSWORD}';

  GRANT CONNECT ON DATABASE ${POSTGRES_DB} TO saapre_migrator, saapre_app;
  GRANT USAGE ON SCHEMA public TO saapre_app;
  GRANT USAGE, CREATE ON SCHEMA public TO saapre_migrator;

  ALTER DEFAULT PRIVILEGES FOR ROLE saapre_migrator IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO saapre_app;
  ALTER DEFAULT PRIVILEGES FOR ROLE saapre_migrator IN SCHEMA public
    GRANT USAGE, SELECT ON SEQUENCES TO saapre_app;
EOSQL
