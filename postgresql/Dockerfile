FROM postgres:15

WORKDIR /docker-entrypoint-initdb.d

COPY init.sql .

CMD ["postgres"]