FROM postgres:17.0

COPY ../backend/init.sql /docker-entrypoint-initdb.d/init.sql
RUN mkdir -p /data/pg
