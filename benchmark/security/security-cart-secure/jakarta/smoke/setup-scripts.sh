#!/bin/bash

# Setup script to copy all verification scripts to the GlassFish container
# Usage: ./setup-scripts.sh

set -e

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "SUCCESS")
            echo -e "${GREEN}✓${NC} $message"
            ;;
        "WARNING")
            echo -e "${YELLOW}⚠${NC} $message"
            ;;
        "ERROR")
            echo -e "${RED}✗${NC} $message"
            ;;
    esac
}

echo "=== Cart EJB Verification Scripts Setup ==="
echo

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    print_status "ERROR" "docker-compose command not found"
    echo "Please install Docker Compose to continue"
    exit 1
fi

# Check if we're in the right directory and find docker-compose.yml
if [ -f "docker-compose.yml" ]; then
    # Already in the right directory
    print_status "SUCCESS" "Found docker-compose.yml in current directory"
elif [ -f "../docker-compose.yml" ]; then
    # We're in scripts/ directory, go up one level
    cd ..
    print_status "SUCCESS" "Found docker-compose.yml in parent directory"
else
    print_status "ERROR" "docker-compose.yml not found"
    echo "Please run this script from either:"
    echo "  - The main project directory (where docker-compose.yml is located)"
    echo "  - The scripts/ subdirectory"
    exit 1
fi

# Check if container is running
echo "Checking container status..."
CONTAINER_STATUS=$(docker-compose ps -q glassfish 2>/dev/null || echo "")

if [ -z "$CONTAINER_STATUS" ]; then
    print_status "ERROR" "GlassFish container is not running"
    echo "Please start the container first:"
    echo "  docker-compose up -d"
    exit 1
fi

print_status "SUCCESS" "GlassFish container is running"

# List of scripts to copy
SCRIPTS=(
    "check-glassfish-status.sh"
    "list-applications.sh"
    "check-ejb-container.sh"
    "check-ejb-jndi.sh"
    "check-security-config.sh"
    "verify-all.sh"
)

echo
echo "Copying verification scripts to container..."

# Copy each script
for script in "${SCRIPTS[@]}"; do
    script_path="smoke/$script"

    if [ -f "$script_path" ]; then
        echo "Copying $script..."

        # Copy script to container
        if docker cp "$script_path" security-cart-secure-glassfish-1:/tmp/; then
            # Make script executable
            if docker-compose exec -T glassfish chmod +x "/tmp/$script"; then
                print_status "SUCCESS" "$script copied and made executable"
            else
                print_status "ERROR" "Failed to make $script executable"
            fi
        else
            print_status "ERROR" "Failed to copy $script"
        fi
    else
        print_status "ERROR" "$script not found in scripts directory"
    fi
done

echo
echo "=== Setup Summary ==="

# Verify all scripts are in container
echo "Verifying scripts in container..."
MISSING_SCRIPTS=()

for script in "${SCRIPTS[@]}"; do
    if docker-compose exec -T glassfish test -f "/tmp/$script" && docker-compose exec -T glassfish test -x "/tmp/$script"; then
        print_status "SUCCESS" "$script is present and executable"
    else
        print_status "ERROR" "$script is missing or not executable"
        MISSING_SCRIPTS+=("$script")
    fi
done

echo

if [ ${#MISSING_SCRIPTS[@]} -eq 0 ]; then
    print_status "SUCCESS" "All scripts successfully copied to container"
    echo
    echo "=== How to Use the Scripts ==="
    echo
    echo "1. Run complete verification:"
    echo "   docker-compose exec -T glassfish /tmp/verify-all.sh"
    echo
    echo "2. Run individual checks:"
    echo "   docker-compose exec -T glassfish /tmp/check-glassfish-status.sh"
    echo "   docker-compose exec -T glassfish /tmp/list-applications.sh"
    echo "   docker-compose exec -T glassfish /tmp/check-ejb-container.sh"
    echo "   docker-compose exec -T glassfish /tmp/check-ejb-jndi.sh"
    echo "   docker-compose exec -T glassfish /tmp/check-security-config.sh"
    echo
    echo "3. Interactive mode (run multiple commands):"
    echo "   docker-compose exec glassfish bash"
    echo "   # Then inside container:"
    echo "   /tmp/verify-all.sh"
    echo
    echo "=== Quick Test ==="
    echo "Running a quick verification test..."
    echo

    # Run the master verification script
    if docker-compose exec -T glassfish /tmp/verify-all.sh; then
        echo
        print_status "SUCCESS" "All verification scripts are working correctly!"
        echo "Cart EJB application is ready for testing."
    else
        echo
        print_status "WARNING" "Verification completed with some issues"
        echo "Check the output above for details."
    fi
else
    print_status "ERROR" "Setup incomplete - ${#MISSING_SCRIPTS[@]} script(s) failed to copy"
    echo "Missing scripts: ${MISSING_SCRIPTS[*]}"
    echo
    echo "Troubleshooting:"
    echo "• Ensure container is running: docker-compose ps"
    echo "• Check container logs: docker-compose logs glassfish"
    echo "• Verify scripts exist in scripts/ directory"
    echo "• Try running setup again: ./setup-scripts.sh"
    exit 1
fi

echo
echo "=== Setup Complete ==="
print_status "SUCCESS" "Verification scripts are ready to use!"
