# Simple runtime-only image; copy your built Spring Boot fat-jar
FROM eclipse-temurin:21-jre
WORKDIR /app
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} app.jar
ENV SPRING_PROFILES_ACTIVE=docker
# no external port needed
ENTRYPOINT ["java","-jar","/app/app.jar"]
