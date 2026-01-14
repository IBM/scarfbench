# Multi-stage build: Build stage
FROM eclipse-temurin:11-jdk AS builder

# Install Maven
RUN apt-get update && apt-get install -y maven && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy source code and Maven wrapper
COPY . .

# Make Maven wrapper executable
RUN chmod +x mvnw

# Build the project
RUN ./mvnw clean package -DskipTests

# Runtime stage
FROM eclipse-temurin:11-jre

# Install curl and unzip
RUN apt-get update && apt-get install -y curl unzip && rm -rf /var/lib/apt/lists/*

# Set GlassFish version
ENV GLASSFISH_VERSION=7.0.16

# Download and install GlassFish
RUN curl -L -o /tmp/glassfish.zip https://github.com/eclipse-ee4j/glassfish/releases/download/${GLASSFISH_VERSION}/glassfish-${GLASSFISH_VERSION}.zip && \
    unzip /tmp/glassfish.zip -d /opt && \
    rm /tmp/glassfish.zip && \
    mv /opt/glassfish7 /opt/glassfish

# Set environment variables
ENV GLASSFISH_HOME=/opt/glassfish
ENV PATH=$PATH:$GLASSFISH_HOME/bin

# Configure the default domain to use port 8080 (it already exists)
# We don't need to create a new domain, just use the existing one

# Copy the built WAR file from the builder stage
COPY --from=builder /app/target/timersession.war $GLASSFISH_HOME/glassfish/domains/domain1/autodeploy/timersession.war

# Expose ports
EXPOSE 8080 4848 8181

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "Starting GlassFish domain1..."\n\
asadmin start-domain domain1\n\
echo "GlassFish started successfully"\n\
echo "Application should be available at http://localhost:8080/timersession/"\n\
echo "Admin console available at http://localhost:4848/"\n\
tail -f $GLASSFISH_HOME/glassfish/domains/domain1/logs/server.log' > /start-glassfish.sh && \
    chmod +x /start-glassfish.sh

# Start GlassFish
CMD ["/start-glassfish.sh"]
