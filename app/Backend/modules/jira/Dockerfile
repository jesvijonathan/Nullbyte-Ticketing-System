FROM atlassian/jira-software:latest

ENV MYSQL_JDBC_VERSION=9.0.0
ENV MYSQL_JDBC_URL=https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-j-${MYSQL_JDBC_VERSION}.tar.gz
ENV MYSQL_JDBC_DIR=/opt/atlassian/jira/lib

USER root
RUN apt-get update && \
    apt-get install -y wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN wget ${MYSQL_JDBC_URL} -O /tmp/mysql-connector-j-${MYSQL_JDBC_VERSION}.tar.gz && \
    tar -xzf /tmp/mysql-connector-j-${MYSQL_JDBC_VERSION}.tar.gz -C /tmp && \
    cp /tmp/mysql-connector-j-${MYSQL_JDBC_VERSION}/mysql-connector-j-${MYSQL_JDBC_VERSION}.jar ${MYSQL_JDBC_DIR} && \
    rm -rf /tmp/mysql-connector-j-${MYSQL_JDBC_VERSION}.tar.gz /tmp/mysql-connector-j-${MYSQL_JDBC_VERSION}

RUN chown -R jira:jira ${MYSQL_JDBC_DIR}

USER jira

EXPOSE 8080

CMD ["/opt/atlassian/jira/bin/start-jira.sh", "-fg"]
