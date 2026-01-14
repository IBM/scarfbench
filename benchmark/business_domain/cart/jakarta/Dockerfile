FROM eclipse-temurin:11-jdk

USER root
RUN apt-get update && apt-get install -y python3 curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app

# Copy parent POM and Maven wrapper
COPY --chown=1001:1001 pom.xml .
COPY --chown=1001:1001 .mvn .mvn
COPY --chown=1001:1001 mvnw .
COPY --chown=1001:1001 mvnw.cmd .

# Copy all module directories
COPY --chown=root:root cart-ejb cart-ejb
COPY --chown=root:root cart-web cart-web

# Copy smoke test
COPY --chown=root:root smoke.py .

RUN chmod +x mvnw

# Run Liberty from the cart-web module
CMD ["./mvnw", "clean", "package", "liberty:run"]