FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=root
#ENV MYSQL_DATABASE=nullbyte
#ENV MYSQL_USER=nullbyteadmin
ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_OPTIONS="--secure-file-priv=false"


RUN mkdir -p /var/lib/mysql-files

COPY ./scripts/*.sql /docker-entrypoint-initdb.d/
COPY ./data/*.csv /var/lib/mysql-files/

EXPOSE 3306

CMD ["mysqld"]
