FROM postgres:15

WORKDIR /docker-entrypoint-initdb.d

COPY data.csv .
COPY init.sql .

CMD ["postgres"]