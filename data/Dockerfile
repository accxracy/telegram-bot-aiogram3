FROM postgres:15-alpine

COPY 01_init.sql /docker-entrypoint-initdb.d/01_init.sql
COPY 02_seed.sql /docker-entrypoint-initdb.d/02_seed.sql
EXPOSE 5432
