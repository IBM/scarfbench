#!/bin/bash

# Check EJB JNDI entries and bindings
# Usage: ./check-ejb-jndi.sh

set -e

echo "=== EJB JNDI Verification ==="

# Check if asadmin is available
if ! command -v asadmin &> /dev/null; then
    echo "   ✗ asadmin command not found"
    echo "   Make sure you're running this inside the GlassFish container"
    exit 1
fi

# Check global JNDI namespace
echo "1. Checking global JNDI namespace..."
GLOBAL_ENTRIES=$(asadmin list-jndi-entries --context "java:global" 2>/dev/null | grep -v "Command executed successfully" | grep -v "^$")

if [ -n "$GLOBAL_ENTRIES" ]; then
    echo "   ✓ Global JNDI entries found:"
    echo "$GLOBAL_ENTRIES" | while IFS= read -r entry; do
        if [ -n "$entry" ]; then
            echo "     - $entry"
        fi
    done
else
    echo "   ✗ No global JNDI entries found"
    exit 1
fi

echo

# Look for Cart EJB specifically
echo "2. Searching for Cart EJB entries..."
CART_ENTRIES=$(echo "$GLOBAL_ENTRIES" | grep -i "cart" || echo "")

if [ -n "$CART_ENTRIES" ]; then
    echo "   ✓ Cart EJB application found in JNDI:"
    echo "$CART_ENTRIES" | while IFS= read -r entry; do
        if [ -n "$entry" ]; then
            echo "     - $entry"
        fi
    done

    # Get the first cart application name for detailed inspection
    CART_APP=$(echo "$CART_ENTRIES" | head -1 | cut -d':' -f1)

    echo
    echo "3. Inspecting Cart EJB details..."
    echo "   Application context: java:global/$CART_APP"

    # List Cart application modules
    CART_MODULES=$(asadmin list-jndi-entries --context "java:global/$CART_APP" 2>/dev/null | grep -v "Command executed successfully" | grep -v "^$")

    if [ -n "$CART_MODULES" ]; then
        echo "   ✓ Cart application modules:"
        echo "$CART_MODULES" | while IFS= read -r module; do
            if [ -n "$module" ]; then
                echo "     - $module"
            fi
        done

        # Look for specific EJB beans
        MODULE_NAME=$(echo "$CART_MODULES" | head -1 | cut -d':' -f1)

        echo
        echo "4. Inspecting EJB beans in module: $MODULE_NAME"
        EJB_BEANS=$(asadmin list-jndi-entries --context "java:global/$CART_APP/$MODULE_NAME" 2>/dev/null | grep -v "Command executed successfully" | grep -v "^$")

        if [ -n "$EJB_BEANS" ]; then
            echo "   ✓ EJB beans found:"
            echo "$EJB_BEANS" | while IFS= read -r bean; do
                if [ -n "$bean" ]; then
                    if echo "$bean" | grep -i "cartbean" > /dev/null; then
                        echo "     ✓ $bean"
                    else
                        echo "     - $bean"
                    fi
                fi
            done

            # Extract business interface information
            echo
            echo "5. Business interface analysis..."
            BUSINESS_INTERFACE=$(echo "$EJB_BEANS" | grep "CartBean!" | head -1)
            if [ -n "$BUSINESS_INTERFACE" ]; then
                INTERFACE_NAME=$(echo "$BUSINESS_INTERFACE" | cut -d'!' -f2 | cut -d':' -f1)
                echo "   ✓ Business interface: $INTERFACE_NAME"
                echo "   ✓ JNDI lookup name: java:global/$CART_APP/$MODULE_NAME/CartBean"
                echo "   ✓ Full business interface lookup: java:global/$CART_APP/$MODULE_NAME/CartBean!$INTERFACE_NAME"
            else
                echo "   ⚠ Business interface information not found"
            fi
        else
            echo "   ✗ No EJB beans found in module"
        fi
    else
        echo "   ✗ No modules found in Cart application"
    fi

else
    echo "   ✗ Cart EJB not found in JNDI"
    echo "   Available applications:"
    echo "$GLOBAL_ENTRIES" | while IFS= read -r entry; do
        if [ -n "$entry" ]; then
            echo "     - $entry"
        fi
    done
    exit 1
fi

echo

# Summary
echo "=== JNDI Summary ==="
if [ -n "$CART_ENTRIES" ] && [ -n "$EJB_BEANS" ]; then
    echo "✓ Cart EJB is properly deployed and accessible via JNDI"
    echo "✓ Ready for remote client connections"

    # Show client connection information
    echo
    echo "=== Client Connection Info ==="
    echo "JNDI Context: java:global/$CART_APP/$MODULE_NAME/CartBean"
    if [ -n "$INTERFACE_NAME" ]; then
        echo "Business Interface: $INTERFACE_NAME"
    fi
    echo "Security Role Required: TutorialUser"
    echo "Access Method: Remote EJB via CORBA/IIOP"
else
    echo "✗ Cart EJB deployment issues detected"
    exit 1
fi

echo "=== EJB JNDI Verification Complete ==="
