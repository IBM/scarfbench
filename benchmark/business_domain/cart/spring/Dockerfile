FROM eclipse-temurin:17-jdk

USER root
RUN apt-get update && apt-get install -y python3 curl && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 1001 spring

USER spring
WORKDIR /app

# Copy all project files
COPY --chown=1001:1001 pom.xml .
COPY --chown=1001:1001 .mvn .mvn
COPY --chown=1001:1001 mvnw .
COPY --chown=1001:1001 smoke.py .

# Copy all module directories
# This might be an issue since it's not guaranteed that we'll have the same names
COPY --chown=1001:1001 cart-ejb cart-ejb
COPY --chown=1001:1001 cart-web cart-web

RUN chmod +x mvnw

EXPOSE 8080

# Default command matches your local workflow, couldn't get it working with spring-boot:run
CMD ["sh", "-c", "./mvnw clean package && java -jar cart-web/target/cart-web.jar"]