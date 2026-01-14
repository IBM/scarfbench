FROM icr.io/appcafe/open-liberty:kernel-slim-java21-openj9-ubi-minimal

ARG VERSION=1.0
ARG REVISION=SNAPSHOT

LABEL \
  org.opencontainers.image.authors="appiepollo14" \
  org.opencontainers.image.version="$VERSION" \
  org.opencontainers.image.revision="$REVISION" \
  name="realworld-example" \
  version="$VERSION-$REVISION" \
  summary="The OpenLiberty Realworld example" \
  description="This image contains the Realworld API implementation running with the Open Liberty runtime."

USER root

COPY --chown=1001:0 \
    src/main/liberty/config/ \
    /config/

RUN features.sh

COPY --chown=1001:0 \
    target/realworld-liberty/WEB-INF/lib/postgresql*.jar \
    /config/jdbc/

COPY --chown=1001:0 \
    target/realworld-liberty.war \
    /config/dropins

USER 1001

RUN configure.sh
