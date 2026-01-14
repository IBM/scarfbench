# --------------------------------------------------------------------
# Base image: Maven + JDK 21 for Jakarta EE
# --------------------------------------------------------------------
FROM maven:3.9-eclipse-temurin-21

# We'll work as root for package installs (this is the default in this image)
USER root

# --------------------------------------------------------------------
# System deps: Python, Chromium + driver, curl (for uv installer), and Playwright dependencies
# --------------------------------------------------------------------
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    python3 python3-venv python3-pip \
    curl \
    chromium chromium-driver \
    libglib2.0-0t64 \
    libnspr4 \
    libnss3 \
    libatk1.0-0t64 \
    libatk-bridge2.0-0t64 \
    libcups2t64 \
    libxcb1 \
    libxkbcommon0 \
    libatspi2.0-0t64 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libcairo2 \
    libpango-1.0-0 \
    libasound2t64 \
    && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------
# Install uv (Python package/project manager)
# --------------------------------------------------------------------
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    ln -s /root/.cargo/bin/uv /usr/local/bin/uv

# --------------------------------------------------------------------
# App + smoke project
# --------------------------------------------------------------------
WORKDIR /workspace

# Copy Maven project (multi-module)
COPY pom.xml ./
COPY common ./common
COPY orders-service ./orders-service
COPY barista-service ./barista-service
COPY kitchen-service ./kitchen-service

# Copy smoke test project (uv project with pyproject.toml)
COPY smoke ./smoke

# Optionally pre-resolve Python deps so 'uv run' is fast later:
# RUN cd smoke && uv sync

# Build the Jakarta EE app once during image build
# (use -DskipTests if you want it faster)
# Install common module to local repo so it's available for liberty:dev
RUN mvn -B -DskipTests install

# --------------------------------------------------------------------
# Default command: run the orders-service via Liberty
# Note: This is a multi-service application, typically run via docker-compose
# Install common module first, then run liberty:dev for orders-service
# You can then exec into the container to run:
#   cd smoke && uv sync && uv run playwright install chromium && uv run smoke.py
# --------------------------------------------------------------------
CMD ["sh", "-c", "mvn -pl common install && mvn -pl orders-service liberty:dev"]
