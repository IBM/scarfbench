FROM eclipse-temurin:17-jdk

USER root
RUN apt-get update && apt-get install -y --no-install-recommends python3 curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 1001 spring

USER spring
WORKDIR /app

COPY --chown=1001:1001 pom.xml .
COPY --chown=1001:1001 .mvn .mvn
COPY --chown=1001:1001 mvnw .
COPY --chown=1001:1001 mvnw.cmd .
COPY --chown=1001:1001 roster-boot roster-boot
COPY --chown=1001:1001 roster-common roster-common
COPY --chown=1001:1001 smoke.py .

RUN chmod +x mvnw

RUN ./mvnw clean install -DskipTests

EXPOSE 8080

CMD ["./mvnw", "-pl", "roster-boot", "spring-boot:run"]
