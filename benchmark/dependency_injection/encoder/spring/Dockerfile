FROM openjdk:17-jdk-slim

# set smoke test env variables
ENV ENCODER_BASE_URL=http://localhost:8080
ENV ENCODER_HOME_URI=/encoder

# Install Python (add python3-venv for virtual environment support)
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment for Python dependencies (PEP 668 safe)
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# Shared browsers path so Chromium is cached once
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN mkdir -p /ms-playwright && chmod 755 /ms-playwright

# Install Playwright and Chromium dependencies inside venv
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
 && pip install --no-cache-dir playwright==1.47.0 \
 && playwright install --with-deps chromium

WORKDIR /app

COPY target/encoder.jar app.jar
COPY smoke.py /opt/smoke-test/smoke.py

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
