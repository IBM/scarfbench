FROM icr.io/appcafe/open-liberty:full-java21-openj9-ubi-minimal
COPY --chown=1001:0 src/main/liberty/config/ /config/
RUN rm -f /config/server.env
COPY --chown=1001:0 target/barista-service.war /config/dropins/
ENV WLP_LOGGING_CONSOLE_FORMAT=JSON \
    WLP_LOGGING_CONSOLE_LOGLEVEL=INFO \
    WLP_LOGGING_CONSOLE_SOURCE=message,trace,accessLog,ffdc
