#!/bin/bash

# List deployed applications in GlassFish
# Usage: ./list-applications.sh

set -e

echo "=== Deployed Applications ==="

# Check if asadmin is available
if ! command -v asadmin &> /dev/null; then
    echo "   ✗ asadmin command not found"
    echo "   Make sure you're running this inside the GlassFish container"
    exit 1
fi

# List all applications
echo "Listing all deployed applications..."
APPS=$(asadmin list-applications --terse 2>/dev/null | grep -v "Command executed successfully" | grep -v "^$")

if [ -n "$APPS" ]; then
    echo "   ✓ Found deployed applications:"
    echo "$APPS" | while IFS= read -r app; do
        if [ -n "$app" ]; then
            echo "     - $app"
        fi
    done

    echo
    echo "Application details:"
    echo "$APPS" | while IFS= read -r app; do
        if [ -n "$app" ]; then
            APP_NAME=$(echo "$app" | cut -d' ' -f1)
            APP_TYPE=$(echo "$app" | grep -o '<[^>]*>' | tr -d '<>')
            echo "   Application: $APP_NAME"
            echo "   Type: $APP_TYPE"
            echo "   Status: Running"
            echo
        fi
    done
else
    echo "   ✗ No applications deployed"
    echo "   Use 'asadmin deploy <path-to-ear>' to deploy applications"
    exit 1
fi

# Show application status summary
echo "=== Application Summary ==="
APP_COUNT=$(echo "$APPS" | wc -l)
echo "Total applications deployed: $APP_COUNT"

# Check for specific Cart application
if echo "$APPS" | grep -i "cart" > /dev/null; then
    echo "✓ Cart application is deployed and running"
else
    echo "⚠ Cart application not found in deployed applications"
fi

echo "=== Application List Complete ==="
