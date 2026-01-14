#!/bin/bash

# Check security configuration for EJB applications
# Usage: ./check-security-config.sh

set -e

echo "=== Security Configuration Check ==="

# Check if asadmin is available
if ! command -v asadmin &> /dev/null; then
    echo "   ✗ asadmin command not found"
    echo "   Make sure you're running this inside the GlassFish container"
    exit 1
fi

# Check security service status
echo "1. Checking security service status..."
SECURITY_SERVICE=$(asadmin get configs.config.server-config.security-service.activate-default-principal-to-role-mapping 2>/dev/null || echo "")

if [ -n "$SECURITY_SERVICE" ]; then
    echo "   ✓ Security service is accessible"
    echo "   Principal-to-role mapping: $SECURITY_SERVICE"
else
    echo "   ⚠ Security service configuration not accessible"
fi

echo

# Check default realm configuration
echo "2. Checking default security realm..."
DEFAULT_REALM=$(asadmin get server.security-service.default-realm 2>/dev/null | cut -d'=' -f2 || echo "unknown")

if [ "$DEFAULT_REALM" != "unknown" ]; then
    echo "   ✓ Default realm configured: $DEFAULT_REALM"

    # Get realm details
    REALM_DETAILS=$(asadmin get configs.config.server-config.security-service.auth-realm.$DEFAULT_REALM.* 2>/dev/null | grep -v "Command get executed successfully" || echo "")

    if [ -n "$REALM_DETAILS" ]; then
        echo "   ✓ Realm details:"
        echo "$REALM_DETAILS" | while IFS= read -r detail; do
            if [ -n "$detail" ]; then
                if echo "$detail" | grep -q "classname"; then
                    echo "     ✓ $detail"
                elif echo "$detail" | grep -q "file"; then
                    echo "     ✓ $detail"
                else
                    echo "     - $detail"
                fi
            fi
        done
    else
        echo "   ⚠ Could not retrieve realm details"
    fi
else
    echo "   ✗ Default realm not configured properly"
fi

echo

# List all available realms
echo "3. Listing all security realms..."
REALMS=$(asadmin list-auth-realms 2>/dev/null | grep -v "Command executed successfully" | grep -v "^$" || echo "")

if [ -n "$REALMS" ]; then
    echo "   ✓ Available realms:"
    echo "$REALMS" | while IFS= read -r realm; do
        if [ -n "$realm" ]; then
            if [ "$realm" = "$DEFAULT_REALM" ]; then
                echo "     ✓ $realm (default)"
            else
                echo "     - $realm"
            fi
        fi
    done
else
    echo "   ✗ No security realms found"
fi

echo

# Check JACC configuration
echo "4. Checking JACC (Java Authorization Contract for Containers)..."
JACC_PROVIDER=$(asadmin get configs.config.server-config.security-service.jacc 2>/dev/null | cut -d'=' -f2 || echo "unknown")

if [ "$JACC_PROVIDER" != "unknown" ]; then
    echo "   ✓ JACC provider: $JACC_PROVIDER"
else
    echo "   ⚠ JACC configuration not accessible"
fi

echo

# Check role mapping configuration
echo "5. Checking role mapping settings..."
ROLE_MAPPING=$(asadmin get configs.config.server-config.security-service.activate-default-principal-to-role-mapping 2>/dev/null | cut -d'=' -f2 || echo "unknown")

if [ "$ROLE_MAPPING" != "unknown" ]; then
    echo "   ✓ Default principal-to-role mapping: $ROLE_MAPPING"

    if [ "$ROLE_MAPPING" = "true" ]; then
        echo "   ✓ Automatic role mapping is enabled"
    else
        echo "   ⚠ Automatic role mapping is disabled"
        echo "     You may need to configure role mappings manually"
    fi
else
    echo "   ⚠ Role mapping configuration not accessible"
fi

echo

# Check SSL/TLS configuration
echo "6. Checking SSL/TLS configuration..."
SSL_CONFIG=$(asadmin get configs.config.server-config.network-config.protocols.protocol.sec-admin-listener.ssl.* 2>/dev/null | head -3 | grep -v "Command get executed successfully" || echo "")

if [ -n "$SSL_CONFIG" ]; then
    echo "   ✓ SSL configuration found:"
    echo "$SSL_CONFIG" | while IFS= read -r config; do
        if [ -n "$config" ]; then
            echo "     - $config"
        fi
    done
else
    echo "   ⚠ SSL configuration not accessible"
fi

echo

# Check security for EJB applications specifically
echo "7. Checking EJB security configuration..."
EJB_SECURITY=$(asadmin get configs.config.server-config.ejb-container.* 2>/dev/null | grep -i security | head -3 || echo "")

if [ -n "$EJB_SECURITY" ]; then
    echo "   ✓ EJB security settings:"
    echo "$EJB_SECURITY" | while IFS= read -r setting; do
        if [ -n "$setting" ]; then
            echo "     - $setting"
        fi
    done
else
    echo "   ⚠ EJB-specific security settings not found"
fi

echo

# Check for Cart application security roles
echo "8. Checking Cart application security roles..."
# Look for deployed applications first
CART_APP=$(asadmin list-applications --terse 2>/dev/null | grep -i cart | head -1 | cut -d' ' -f1 || echo "")

if [ -n "$CART_APP" ]; then
    echo "   ✓ Cart application found: $CART_APP"

    # Try to get application-specific security info
    APP_SECURITY=$(asadmin get applications.application.$CART_APP.* 2>/dev/null | grep -i security || echo "")

    if [ -n "$APP_SECURITY" ]; then
        echo "   ✓ Application security configuration:"
        echo "$APP_SECURITY" | while IFS= read -r config; do
            if [ -n "$config" ]; then
                echo "     - $config"
            fi
        done
    else
        echo "   ⚠ No application-specific security configuration found"
        echo "   ✓ Using container default security settings"
    fi
else
    echo "   ⚠ Cart application not currently deployed"
fi

echo

# Security summary and recommendations
echo "=== Security Configuration Summary ==="

if [ "$DEFAULT_REALM" != "unknown" ] && [ -n "$REALMS" ]; then
    echo "✓ Security realms are properly configured"
    echo "✓ Default realm: $DEFAULT_REALM"

    if [ "$ROLE_MAPPING" = "true" ]; then
        echo "✓ Automatic role mapping is enabled"
        echo "  EJB @RolesAllowed annotations will be enforced"
    else
        echo "⚠ Manual role mapping may be required"
        echo "  Check application-specific security mappings"
    fi

    if [ "$JACC_PROVIDER" != "unknown" ]; then
        echo "✓ JACC authorization is configured"
    fi

    echo "✓ Security service is operational for EJB applications"
else
    echo "✗ Security configuration issues detected"
    echo "  Review realm and security service settings"
    exit 1
fi

echo

echo "=== Security Requirements for Cart EJB ==="
echo "Required security role: TutorialUser"
echo "Authentication realm: $DEFAULT_REALM"
echo "Authorization method: @RolesAllowed annotation"
echo "Security applied to: addBook, removeBook, getContents, remove methods"
echo ""
echo "To test with authentication:"
echo "1. Create user in $DEFAULT_REALM realm"
echo "2. Assign TutorialUser role to the user"
echo "3. Configure client with proper credentials"

echo "=== Security Configuration Check Complete ==="
