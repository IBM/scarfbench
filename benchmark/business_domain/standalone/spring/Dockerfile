FROM eclipse-temurin:17-jdk

USER root
RUN apt-get update && apt-get install -y python3 curl && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 1001 spring

# set smoke test env variables
ENV BASE_URL=http://localhost:8080/standalone

USER spring
WORKDIR /app

# Copy all project files
COPY --chown=1001:1001 pom.xml .
COPY --chown=1001:1001 .mvn .mvn
COPY --chown=1001:1001 mvnw .
COPY --chown=1001:1001 src src
COPY --chown=1001:1001 smoke.py .

RUN chmod +x mvnw

EXPOSE 8080

# Default command matches your local workflow
CMD ["./mvnw", "clean", "package", "spring-boot:run"]