FROM eclipse-temurin:11-jdk

USER root
RUN apt-get update && apt-get install -y python3 curl && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 1001 liberty

# set smoke test env variables
ENV HELLO_SERVICE_URL=http://localhost:9080/helloservice/HelloServiceBeanService

USER liberty
WORKDIR /app

# Copy parent POM and Maven wrapper
COPY --chown=1001:1001 pom.xml .
COPY --chown=1001:1001 .mvn .mvn
COPY --chown=1001:1001 mvnw .
COPY --chown=1001:1001 mvnw.cmd .
COPY --chown=1001:1001 src src
COPY --chown=1001:1001 smoke.py .

RUN chmod +x mvnw

EXPOSE 9080

# Default command matches your local workflow
CMD ["./mvnw", "clean", "package", "liberty:run"]