#!/bin/bash

# Check EJB container status and configuration
# Usage: ./check-ejb-container.sh

set -e

echo "=== EJB Container Status Check ==="
# Check if asadmin is available
if ! command -v asadmin &> /dev/null; then
    echo "   ✗ asadmin command not found"
    echo "   Make sure you're running this inside the GlassFish container"
    exit 1
fi

# Check EJB container status
echo "1. Checking EJB container status..."
EJB_CONTAINER=$(asadmin list-containers 2>/dev/null | grep -i ejb || echo "")

if [ -n "$EJB_CONTAINER" ]; then
    echo "   ✓ EJB Container is active"
    echo "   Container info: $EJB_CONTAINER"
else
    echo "   ✗ EJB Container status unknown or not active"
    echo "   Available containers:"
    asadmin list-containers 2>/dev/null | while IFS= read -r container; do
        if [ -n "$container" ] && [ "$container" != "Command list-containers executed successfully." ]; then
            echo "     - $container"
        fi
    done
fi

echo

# Check EJB-related resources
echo "2. Checking EJB resources and pools..."
EJB_RESOURCES=$(asadmin list-resources 2>/dev/null | grep -i ejb || echo "")

if [ -n "$EJB_RESOURCES" ]; then
    echo "   ✓ EJB-related resources found:"
    echo "$EJB_RESOURCES" | while IFS= read -r resource; do
        if [ -n "$resource" ]; then
            echo "     - $resource"
        fi
    done
else
    echo "   ⚠ No specific EJB resources found (this may be normal)"
fi

echo

# Check ORB (Object Request Broker) configuration for remote EJB access
echo "3. Checking ORB configuration..."
ORB_CONFIG=$(asadmin get configs.config.server-config.orb.* 2>/dev/null | grep -v "Command get executed successfully" || echo "")

if [ -n "$ORB_CONFIG" ]; then
    echo "   ✓ ORB configuration found:"
    echo "$ORB_CONFIG" | while IFS= read -r config; do
        if [ -n "$config" ]; then
            # Extract key configuration values
            if echo "$config" | grep -q "iiop-port"; then
                echo "     ✓ $config"
            elif echo "$config" | grep -q "ssl-port"; then
                echo "     ✓ $config"
            else
                echo "     - $config"
            fi
        fi
    done
else
    echo "   ⚠ ORB configuration not accessible"
fi

echo

# Check IIOP listeners for remote EJB access
echo "4. Checking IIOP listeners..."
IIOP_LISTENERS=$(asadmin list-iiop-listeners 2>/dev/null | grep -v "Command executed successfully" | grep -v "^$" || echo "")

if [ -n "$IIOP_LISTENERS" ]; then
    echo "   ✓ IIOP listeners configured:"
    echo "$IIOP_LISTENERS" | while IFS= read -r listener; do
        if [ -n "$listener" ]; then
            echo "     ✓ $listener"
        fi
    done
else
    echo "   ⚠ No IIOP listeners found"
    echo "   Remote EJB access may not be available"
fi

echo

# Check transaction service (important for EJBs)
echo "5. Checking transaction service..."
TX_SERVICE=$(asadmin get configs.config.server-config.transaction-service.* 2>/dev/null | grep -v "Command get executed successfully" | head -5 || echo "")

if [ -n "$TX_SERVICE" ]; then
    echo "   ✓ Transaction service configured:"
    echo "$TX_SERVICE" | while IFS= read -r config; do
        if [ -n "$config" ]; then
            if echo "$config" | grep -q "automatic-recovery"; then
                echo "     ✓ $config"
            elif echo "$config" | grep -q "timeout-in-seconds"; then
                echo "     ✓ $config"
            else
                echo "     - $config"
            fi
        fi
    done
else
    echo "   ⚠ Transaction service configuration not accessible"
fi

echo

# Check EJB timer service
echo "6. Checking EJB timer service..."
TIMER_SERVICE=$(asadmin get configs.config.server-config.ejb-container.ejb-timer-service.* 2>/dev/null | grep -v "Command get executed successfully" | head -3 || echo "")

if [ -n "$TIMER_SERVICE" ]; then
    echo "   ✓ EJB timer service configured:"
    echo "$TIMER_SERVICE" | while IFS= read -r config; do
        if [ -n "$config" ]; then
            echo "     - $config"
        fi
    done
else
    echo "   ⚠ EJB timer service configuration not accessible"
fi

echo

# Summary and recommendations
echo "=== EJB Container Summary ==="

if [ -n "$EJB_CONTAINER" ]; then
    echo "✓ EJB Container is operational"

    if [ -n "$IIOP_LISTENERS" ]; then
        echo "✓ Remote EJB access is configured"
        echo "✓ Clients can connect via CORBA/IIOP"
    else
        echo "⚠ Remote EJB access may be limited"
        echo "  Consider configuring IIOP listeners for remote clients"
    fi

    if [ -n "$TX_SERVICE" ]; then
        echo "✓ Transaction support is available"
    else
        echo "⚠ Transaction service status unclear"
    fi

    echo "✓ Ready for EJB deployments and operations"
else
    echo "✗ EJB Container issues detected"
    echo "  Check GlassFish configuration and logs"
    exit 1
fi

echo

echo "=== Connection Information ==="
echo "For remote EJB clients:"
echo "  - IIOP Port: Check ORB configuration above"
echo "  - Protocol: CORBA/IIOP"
echo "  - Context Factory: com.sun.enterprise.naming.SerialInitContextFactory"
echo "  - Initial Context: iiop://localhost:3700 (default)"

echo "=== EJB Container Check Complete ==="
