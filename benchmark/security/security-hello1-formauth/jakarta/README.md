# Jakarta EE Security API Example

A demonstration application showcasing Jakarta EE Security API features with database-backed identity store using GlassFish 7 and Derby database.

## Overview

This application demonstrates:
- **Database Identity Store**: User credentials stored in Derby database with PBKDF2 password hashing
- **Basic Authentication**: HTTP Basic authentication mechanism
- **Role-Based Access Control**: Servlet protected by role-based security constraints
- **Auto-Deployment**: WAR deployment to GlassFish application server

## Architecture

- **Application Server**: Eclipse GlassFish 7.0.16
- **Database**: Apache Derby (embedded)
- **Security**: Jakarta EE Security API with database identity store
- **Authentication**: HTTP Basic Authentication
- **Password Hashing**: PBKDF2WithHmacSHA512

## Exposed Ports

| Port  | Service                    | Description                    |
|-------|----------------------------|--------------------------------|
| 10091 | Application HTTP           | Main application endpoint      |
| 10157 | GlassFish Admin Console    | Server administration          |
| 10189 | Application HTTPS          | Secure application endpoint    |

## Quick Start

### Prerequisites
- Docker and Docker Compose

### Deployment Instructions

1. **Build and Deploy**:
   ```bash
   just deploy
   ```

   Or manually:
   ```bash
   docker-compose up -d
   docker-compose exec -T glassfish asadmin start-database
   docker-compose exec -T glassfish asadmin deploy /opt/glassfish/glassfish/domains/domain1/autodeploy/built-in-db-identity-store-10-SNAPSHOT.war
   ```

2. **Verify Deployment**:
   ```bash
   docker-compose exec -T glassfish asadmin list-applications
   ```

3. **Check Application Status**:
   ```bash
   just status
   ```

## Test Users

The application pre-configures the following test users:

| Username | Password | Roles     |
|----------|----------|-----------|
| Joe      | secret1  | foo, bar  |
| Sam      | secret2  | foo, bar  |
| Tom      | secret2  | foo       |
| Sue      | secret2  | foo       |

## API Endpoints & Testing

### Available Endpoints

| Endpoint | Method | Authentication | Required Role | Description |
|----------|--------|----------------|---------------|-------------|
| `/servlet` | GET | Basic Auth | foo | Returns user info and role membership |

### Test Commands

| Test Case | Command | Expected Response Code | Expected Response |
|-----------|---------|----------------------|-------------------|
| **Valid Authentication (Joe)** | `curl -u Joe:secret1 http://localhost:10091/hello1-formauth/servlet` | 200 | User info with roles foo, bar |
| **Valid Authentication (Sam)** | `curl -u Sam:secret2 http://localhost:10091/hello1-formauth/servlet` | 200 | User info with roles foo, bar |
| **Valid Authentication (Tom)** | `curl -u Tom:secret2 http://localhost:10091/hello1-formauth/servlet` | 200 | User info with role foo |
| **Valid Authentication (Sue)** | `curl -u Sue:secret2 http://localhost:10091/hello1-formauth/servlet` | 200 | User info with role foo |
| **No Authentication** | `curl http://localhost:10091/hello1-formauth/servlet` | 401 | Unauthorized - Basic auth required |
| **Invalid Credentials** | `curl -u invalid:wrong http://localhost:10091/hello1-formauth/servlet` | 401 | Unauthorized - Invalid credentials |
| **Non-existent Path** | `curl http://localhost:10091/hello1-formauth/` | 404 | Not Found |

### Sample Response (Valid Authentication)

```
web username: Joe
web user has role "foo": true
web user has role "bar": true
web user has role "kaz": false
```

## Management Commands

| Command | Description |
|---------|-------------|
| `just build` | Build WAR file |
| `just deploy` | Build and deploy application |
| `just up` | Start services |
| `just down` | Stop services |
| `just logs` | View application logs |
| `just status` | Check service status |
| `just restart` | Restart application |

## Security Configuration

### Identity Store Configuration

- **Caller Query**: `select password from caller where name = ?`
- **Groups Query**: `select group_name from caller_groups where caller_name = ?`
- **Hash Algorithm**: PBKDF2WithHmacSHA512
- **Iterations**: 3072
- **Salt Size**: 64 bytes

### Database Schema

```sql
-- Users table
CREATE TABLE caller(
    name VARCHAR(64) PRIMARY KEY,
    password VARCHAR(255)
);

-- Roles table
CREATE TABLE caller_groups(
    caller_name VARCHAR(64),
    group_name VARCHAR(64)
);
```

## Troubleshooting

### Common Issues

1. **Application fails to deploy**:
   - Ensure Derby database is started: `docker-compose exec -T glassfish asadmin start-database`
   - Check deployment status: `docker-compose exec -T glassfish asadmin list-applications`

2. **401 Unauthorized with valid credentials**:
   - Verify user exists in database
   - Check password hash algorithm configuration

3. **404 Not Found**:
   - Use correct application path: `/built-in-db-identity-store-10-SNAPSHOT/servlet`
   - Verify application is deployed

### Health Checks

```bash
# Check container status
docker-compose ps

# Check Derby database
docker-compose exec -T glassfish asadmin ping-connection-pool DerbyPool

# Check application deployment
docker-compose exec -T glassfish asadmin list-applications

# View recent logs
docker-compose logs --tail=50
```

## Development

### Building Locally

```bash
# Build WAR file
./mvnw clean package

# Build Docker image
docker build -t security-api-glassfish:latest .
```

### Project Structure

```
├── built-in-db-identity-store/          # Main application module
│   └── src/main/java/jakarta/tutorial/built_in_db_identity_store/
│       ├── ApplicationConfig.java       # Security configuration
│       ├── DatabaseSetup.java          # Database initialization
│       └── Servlet.java                # Protected servlet
├── custom-identity-store/               # Alternative implementation
├── docker-compose.yml                  # Container orchestration
├── Dockerfile                          # Application container
└── justfile                           # Build automation
```

## License

Eclipse Distribution License v1.0
