FROM eclipse-temurin:17-jdk AS builder

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
FROM eclipse-temurin:17-jre

# Install curl and unzip
RUN apt-get update && apt-get install -y curl unzip python3 && rm -rf /var/lib/apt/lists/*

# Download and install GlassFish
RUN curl -L -o /tmp/glassfish.zip https://github.com/eclipse-ee4j/glassfish/releases/download/7.0.0/glassfish-7.0.0.zip && \
    unzip /tmp/glassfish.zip -d /opt && \
    rm /tmp/glassfish.zip && \
    mv /opt/glassfish7 /opt/glassfish

# Set environment variables
ENV GLASSFISH_HOME=/opt/glassfish
ENV PATH=$PATH:$GLASSFISH_HOME/bin

# Copy the built WAR file
COPY --from=builder /app/target/address-book-10-SNAPSHOT.war $GLASSFISH_HOME/glassfish/domains/domain1/autodeploy/address-book-10-SNAPSHOT.war

# Copy smoke test
COPY --from=builder /app/smoke.py /smoke.py

# Expose ports
EXPOSE 8080 4848 8181 1527

# Create a startup script
RUN echo '#!/bin/bash\n\
echo "Starting Derby database..."\n\
$GLASSFISH_HOME/javadb/bin/startNetworkServer -h 0.0.0.0 -p 1527 &\n\
sleep 5\n\
echo "Starting GlassFish domain1..."\n\
asadmin start-domain domain1\n\
echo "GlassFish started successfully"\n\
echo "Application should be available at http://localhost:8080/address-book-10-SNAPSHOT/"\n\
echo "Admin console available at http://localhost:4848/"\n\
tail -f $GLASSFISH_HOME/glassfish/domains/domain1/logs/server.log' > /start-glassfish.sh && \
    chmod +x /start-glassfish.sh

# Start GlassFish
CMD ["/start-glassfish.sh"]

