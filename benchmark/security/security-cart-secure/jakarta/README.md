# Jakarta EE Cart Secure EJB Application

A demonstration Enterprise Application showcasing Jakarta EE Security features with role-based access control using EJBs, GlassFish 7, and stateful session beans.

## Overview

This application demonstrates:
- **Enterprise Java Beans (EJBs)**: Stateful session bean for shopping cart functionality
- **Role-Based Security**: Method-level security with `@RolesAllowed` annotations
- **JNDI Lookup**: Remote EJB access via Java Naming and Directory Interface
- **Stateful Session Management**: Cart state maintained across multiple client calls
- **Enterprise Archive (EAR)**: Multi-module enterprise application packaging

## Architecture

- **Application Server**: Eclipse GlassFish 7.0.16
- **EJB Container**: Stateful session beans with security
- **Security**: Jakarta EE Security API with declarative role-based access control
- **Packaging**: Enterprise Archive (EAR) with EJB module
- **Client Access**: JNDI-based remote EJB invocation

## Project Structure

```
├── cart-secure-common/          # Shared interfaces and utilities
│   └── src/main/java/jakarta/tutorial/cartsecure/
│       ├── ejb/Cart.java        # Business interface for cart operations
│       └── util/               # Utility classes (BookException, IdVerifier)
├── cart-secure-ejb/            # EJB implementation module
│   └── src/main/java/jakarta/tutorial/cartsecure/ejb/
│       └── CartBean.java       # Stateful session bean implementation
├── cart-secure-appclient/      # Application client (disabled due to Java 11+ compatibility issues)
├── cart-secure-ear/            # Enterprise Archive packaging
└── pom.xml                     # Parent POM with Jakarta EE dependencies
```

## EJB Details

### CartBean Stateful Session Bean

**JNDI Name**: `java:global/cart-secure-ejb-only/jakarta.examples.tutorial.security.cart-secure-cart-secure-ejb-10-SNAPSHOT/CartBean`

**Business Interface**: `jakarta.tutorial.cartsecure.ejb.Cart`

**Security Role**: `TutorialUser` (required for all operations except initialization)

### Available Operations

| Method | Security | Description |
|--------|----------|-------------|
| `initialize(String person)` | None | Initialize cart for a user |
| `initialize(String person, String id)` | None | Initialize cart with user validation |
| `addBook(String title)` | `@RolesAllowed("TutorialUser")` | Add a book to the cart |
| `removeBook(String title)` | `@RolesAllowed("TutorialUser")` | Remove a book from the cart |
| `getContents()` | `@RolesAllowed("TutorialUser")` | Get list of books in cart |
| `remove()` | `@RolesAllowed("TutorialUser")` | Clean up and remove cart |

## Exposed Ports

| Port  | Service                    | Description                    |
|-------|----------------------------|--------------------------------|
| 10088 | GlassFish HTTP             | Application server HTTP port  |
| 10154 | GlassFish Admin Console    | Server administration          |
| 10186 | GlassFish HTTPS            | Secure application endpoint    |
| 3700  | CORBA/IIOP                 | EJB remote invocation          |

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Java 11+ (for client development)

### Deployment Instructions

All verification scripts require the application to be deployed and running first!

1. **Build and Deploy**:
   ```bash
   just deploy
   ```

   Or manually:
   ```bash
   ./mvnw clean package
   docker-compose up -d
   ```

2. **Verify Deployment Success**:
   ```bash
   # Check container is running
   docker-compose ps
   
   # Check application is deployed
   just list-apps
   ```

3. **Setup Verification Scripts** (one-time):
   ```bash
   just setup-scripts
   ```

4. **Run Verification**:
   ```bash
   just verify
   # OR interactive menu
   just menu
   ```

## Testing the EJB

⚠️ **PREREQUISITE**: Application must be deployed and running before testing!

```bash
# 1. First ensure application is deployed
just deploy                 # Build and deploy
just list-apps             # Verify deployment

# 2. Then setup verification scripts (one-time)
just setup-scripts

# 3. Now you can test
```

### Option 1: Interactive Verification Menu (Recommended)

```bash
# Launch interactive menu (after deployment)
just menu
```

The interactive menu provides:
- Complete verification with detailed results
- Individual component checks (GlassFish, EJB, JNDI, Security)
- Connection information and help
- Container logs and interactive shell access

### Option 2: Command Line Verification

```bash
# Run complete verification
just verify

# Run individual checks
just verify-glassfish    # Check GlassFish server status
just verify-apps         # List deployed applications  
just verify-ejb          # Check EJB container status
just verify-jndi         # Check JNDI bindings
just verify-security     # Check security configuration
```

### Option 3: Manual Script Execution

```bash
# Copy scripts to container (one-time setup)
just setup-scripts

# Run verification scripts directly
docker-compose exec -T glassfish /tmp/verify-all.sh
docker-compose exec -T glassfish /tmp/check-ejb-jndi.sh
docker-compose exec -T glassfish /tmp/check-security-config.sh
```

### Option 4: Using GlassFish Admin Console

1. Access the admin console: http://localhost:10154/
2. Navigate to Applications → Enterprise Applications
3. Verify `cart-secure-ejb-only` is listed and enabled

### Option 5: Manual JNDI Verification

```bash
# List JNDI entries
just show-jndi

# Check specific EJB bindings
docker-compose exec -T glassfish asadmin list-jndi-entries \
  --context "java:global/cart-secure-ejb-only/jakarta.examples.tutorial.security.cart-secure-cart-secure-ejb-10-SNAPSHOT"
```

### Option 6: Create a Client Application

To create a client that can invoke the EJB:

1. **Add Dependencies** (Maven):
   ```xml
   <dependency>
       <groupId>org.glassfish.main.appclient</groupId>
       <artifactId>gf-client</artifactId>
       <version>7.0.16</version>
   </dependency>
   <dependency>
       <groupId>jakarta.platform</groupId>
       <artifactId>jakarta.jakartaee-api</artifactId>
       <version>9.0.0</version>
   </dependency>
   ```

2. **JNDI Lookup Example**:
   ```java
   Properties props = new Properties();
   props.setProperty(Context.INITIAL_CONTEXT_FACTORY,
       "com.sun.enterprise.naming.SerialInitContextFactory");
   props.setProperty("org.omg.CORBA.ORBInitialHost", "localhost");
   props.setProperty("org.omg.CORBA.ORBInitialPort", "3700");
   
   InitialContext ctx = new InitialContext(props);
   Cart cart = (Cart) ctx.lookup(
       "java:global/cart-secure-ejb-only/jakarta.examples.tutorial.security.cart-secure-cart-secure-ejb-10-SNAPSHOT/CartBean");
   
   // Use the EJB
   cart.initialize("TestUser", "12345");
   cart.addBook("Jakarta EE 9 Cookbook");
   List<String> books = cart.getContents();
   cart.remove();
   ```

3. **Run with Security Context**:
   ```bash
   java -Djava.security.auth.login.config=login.conf \
        -Djava.security.policy=client.policy \
        YourClientClass
   ```

## Management Commands

| Command | Description |
|---------|-------------|
| `just build` | Build EAR file |
| `just deploy` | Build and deploy application |
| `just setup-scripts` | Copy verification scripts to container (one-time) |
| `just menu` | Launch interactive verification menu |
| `just verify` | Run complete EJB verification |
| `just verify-glassfish` | Check GlassFish server status only |
| `just verify-apps` | Check deployed applications only |
| `just verify-ejb` | Check EJB container status only |
| `just verify-jndi` | Check EJB JNDI bindings only |
| `just verify-security` | Check security configuration only |
| `just list-apps` | List deployed applications |
| `just show-jndi` | Show EJB JNDI entries |
| `just up` | Start services |
| `just down` | Stop services |
| `just logs` | View application logs |
| `just status` | Check service status |
| `just restart` | Restart application |
| `just info` | Show complete application information |
| `just ejb-info` | Show EJB details and methods |

## Security Configuration

### Role-Based Access Control

- **Role Name**: `TutorialUser`
- **Applied To**: All cart operations except initialization
- **Enforcement**: Method-level via `@RolesAllowed` annotation
- **Security Realm**: GlassFish default file realm

### EJB Security Annotations

```java
@Stateful
@DeclareRoles("TutorialUser")
public class CartBean implements Cart {
    
    @Override
    @RolesAllowed("TutorialUser")
    public void addBook(String title) { ... }
    
    @Override
    @RolesAllowed("TutorialUser") 
    public void removeBook(String title) { ... }
    
    // ... other secured methods
}
```

## Troubleshooting

### Common Issues

1. **Verification scripts fail with "No applications deployed"**:
   ```bash
   # SOLUTION: Deploy the application first!
   just deploy                 # Complete build and deploy
   # OR
   just manual-deploy         # Deploy existing EAR
   
   # Then verify deployment
   just list-apps
   ```

2. **Scripts not found in container**:
   ```bash
   # SOLUTION: Setup scripts first
   just setup-scripts
   
   # Then run verification
   just verify
   ```

3. **Application fails to deploy**:
   ```bash
   # Check deployment status
   just list-apps
   
   # Check logs for errors
   just check-logs
   
   # Try manual deployment
   just manual-deploy
   ```

4. **EJB not found in JNDI**:
   ```bash
   # Verify JNDI bindings (only works if app is deployed)
   just show-jndi
   
   # Check EJB container status
   docker-compose exec -T glassfish asadmin list-containers
   ```

3. **Client connection issues**:
   - Ensure CORBA port 3700 is accessible
   - Verify GlassFish is running: `just status`
   - Check network connectivity from client to container

4. **Security exceptions**:
   - Ensure client has proper security credentials
   - Verify role mappings in GlassFish
   - Check security realm configuration

### Known Limitations

1. **Application Client Module**: Disabled due to `jdk.security.jarsigner` compatibility issues with Java 11+ and GlassFish 7
2. **Remote Access**: Requires proper CORBA/IIOP configuration for external clients
3. **Security**: Currently uses default file realm; production deployments should use enterprise security

### Health Checks

⚠️ **Prerequisites**: Container running + Application deployed

```bash
# 1. Basic checks (always run these first)
docker-compose ps                    # Container status
just list-apps                      # Application deployment

# 2. If application is deployed, then run:
just menu                           # Interactive verification
just verify                         # Complete verification

# 3. Individual component checks (require deployed app)
just verify-glassfish              # Server status
just verify-apps                   # Applications
just verify-ejb                    # EJB container  
just verify-jndi                   # JNDI bindings (requires deployed EJB)
just verify-security               # Security config

# 4. Additional checks
docker-compose exec -T glassfish asadmin list-domains  # Domain status
just info                          # Complete application info
```

## Verification Scripts (Smoke Tests)

The application includes comprehensive verification scripts located in `smoke/`:

### Available Scripts

| Script | Purpose |
|--------|---------|
| `setup-scripts.sh` | Copy all smoke test scripts to container and make executable |
| `interactive-menu.sh` | Interactive menu for running verification commands |
| `verify-all.sh` | Master script that runs all verification checks |
| `check-glassfish-status.sh` | Verify GlassFish server is running and accessible |
| `list-applications.sh` | List and analyze deployed applications |
| `check-ejb-container.sh` | Check EJB container status and configuration |
| `check-ejb-jndi.sh` | Verify EJB JNDI bindings and accessibility |
| `check-security-config.sh` | Check security realm and role configuration |

### Script Usage

⚠️ **CRITICAL**: Scripts require deployed application to work!

```bash
# Prerequisite workflow:
just deploy                                    # Deploy application FIRST
just list-apps                                # Verify deployment
just setup-scripts                            # Setup scripts (one-time)

# Then you can run verification:
just menu                                     # Interactive menu
just verify                                   # Complete verification

# Direct script execution (after deployment + setup):
docker-compose exec -T glassfish /tmp/verify-all.sh
docker-compose exec -T glassfish /tmp/check-ejb-jndi.sh
docker-compose exec -T glassfish /tmp/check-security-config.sh

# From inside container (after deployment + setup):
docker-compose exec glassfish bash
/tmp/verify-all.sh
```

### Script Features

- **Color-coded output** with success/warning/error indicators
- **Detailed analysis** of each system component
- **Actionable recommendations** for issues found
- **Complete JNDI path extraction** for client development
- **Security role verification** and configuration analysis
- **Automated container health checks**

## Development

### Building Locally

```bash
# Build EAR file
./mvnw clean package

# Build Docker image
docker build -t security-cart-secure-glassfish:latest .
```

### Modifying the EJB

1. Update business logic in `cart-secure-ejb/src/main/java/jakarta/tutorial/cartsecure/ejb/CartBean.java`
2. Modify interfaces in `cart-secure-common/src/main/java/jakarta/tutorial/cartsecure/ejb/Cart.java`
3. Rebuild and redeploy:
   ```bash
   just deploy
   ```

### Adding Security Roles

1. Update `@DeclareRoles` annotation in CartBean
2. Add `@RolesAllowed` to methods as needed
3. Configure role mappings in GlassFish admin console

## Technical Details

### EJB Lifecycle

1. **Stateful Session Bean**: Maintains conversational state between client calls
2. **JNDI Binding**: Automatically registered in global JNDI namespace
3. **Security Context**: Propagated with each method invocation
4. **Resource Management**: Container-managed lifecycle and transactions

### Container Features Used

- Jakarta EE 9.0 APIs
- EJB 3.2 specification
- CDI for dependency injection
- Jakarta Security for role-based access control
- JNDI for service location

## License

Eclipse Distribution License v1.0

## Notes

- This is an **Enterprise Application**, not a web application
- No HTTP endpoints or servlets are provided
- Access is via EJB remote interfaces through JNDI
- Designed to demonstrate EJB security features and stateful session bean patterns