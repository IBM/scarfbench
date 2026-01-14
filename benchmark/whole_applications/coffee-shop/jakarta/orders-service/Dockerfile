# Base Liberty with Java 21
FROM icr.io/appcafe/open-liberty:full-java21-openj9-ubi-minimal

# Add PostgreSQL JDBC driver (used by orders-service)
ARG PG_JDBC_VER=42.7.3
USER root
RUN mkdir -p /config/lib/global && \
    curl -fsSL -o /config/lib/global/postgresql.jar \
      "https://repo1.maven.org/maven2/org/postgresql/postgresql/${PG_JDBC_VER}/postgresql-${PG_JDBC_VER}.jar"
USER 1001

# Liberty config (server.xml, etc.)
COPY --chown=1001:0 src/main/liberty/config/ /config/
RUN rm -f /config/server.env

# App (expects mvn package already ran)
# COPY --chown=1001:0 target/orders-service.war /config/dropins/
# >>> mount the app via server.xml at contextRoot="/"
# (move from dropins to apps)
COPY --chown=1001:0 target/orders-service.war /config/apps/orders-service.war

# Optional: show default logs on container stdout
ENV WLP_LOGGING_CONSOLE_FORMAT=JSON \
    WLP_LOGGING_CONSOLE_LOGLEVEL=INFO \
    WLP_LOGGING_CONSOLE_SOURCE=message,trace,accessLog,ffdc

