#!/bin/bash

# Check if GlassFish is running
# Usage: ./check-glassfish-status.sh

set -e

echo "=== GlassFish Status Check ==="

# Check if GlassFish process is running
echo "Checking GlassFish process..."
if pgrep -f "glassfish" > /dev/null; then
    echo "   ✓ GlassFish process is running"

    # Get process details
    GLASSFISH_PID=$(pgrep -f "glassfish")
    echo "   Process ID: $GLASSFISH_PID"

    # Check if admin port is responding
    echo "Checking admin port connectivity..."
    if nc -z localhost 4848 2>/dev/null; then
        echo "   ✓ Admin port 4848 is accessible"
    else
        echo "   ⚠ Admin port 4848 is not accessible"
    fi

    # Check if HTTP port is responding
    echo "Checking HTTP port connectivity..."
    if nc -z localhost 8080 2>/dev/null; then
        echo "   ✓ HTTP port 8080 is accessible"
    else
        echo "   ⚠ HTTP port 8080 is not accessible"
    fi

    # Check domain status
    echo "Checking domain status..."
    DOMAIN_STATUS=$(asadmin list-domains 2>/dev/null | grep domain1 || echo "unknown")
    echo "   Domain1 status: $DOMAIN_STATUS"

else
    echo "   ✗ GlassFish is not running"
    exit 1
fi

echo "=== GlassFish Status Check Complete ==="
