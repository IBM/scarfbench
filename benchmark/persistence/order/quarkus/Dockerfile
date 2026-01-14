FROM eclipse-temurin:17-jdk

# Run everything as root
USER root

# Install Python and required tools
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip curl && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Shared browsers path for Playwright
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN mkdir -p /ms-playwright && chmod 755 /ms-playwright

# Install Playwright, aiohttp, and Chromium
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
 && pip install --no-cache-dir playwright==1.47.0 aiohttp \
 && playwright install --with-deps chromium

WORKDIR /app

# Copy Maven wrapper
COPY mvnw .
COPY .mvn .mvn
RUN chmod +x mvnw

# Copy POM for dependency caching
COPY pom.xml .
RUN ./mvnw -q -DskipTests dependency:go-offline || true

# Copy source code
COPY src src
COPY JustFile .
COPY smoke.py .
RUN chmod +x smoke.py

# Build Quarkus application
RUN ./mvnw -q -DskipTests package

# Expose Quarkus port
EXPOSE 8082

# Start Quarkus app, log to file, and run smoke tests
CMD ./mvnw quarkus:run > quarkus.log 2>&1 & sleep 5 && python3 smoke.py