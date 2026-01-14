#!/bin/bash

# Master verification script for Cart EJB Application
# Runs all verification checks in sequence
# Usage: ./verify-all.sh

set -e

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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
        "INFO")
            echo -e "${BLUE}ℹ${NC} $message"
            ;;
    esac
}

# Function to run a script and capture its result
run_check() {
    local script_name=$1
    local description=$2
    local script_path="$SCRIPT_DIR/$script_name"

    echo
    echo "=========================================="
    echo "Running: $description"
    echo "=========================================="

    if [ -f "$script_path" ]; then
        if [ -x "$script_path" ]; then
            if $script_path; then
                print_status "SUCCESS" "$description completed successfully"
                return 0
            else
                print_status "ERROR" "$description failed"
                return 1
            fi
        else
            print_status "ERROR" "$script_path is not executable"
            echo "Run: chmod +x $script_path"
            return 1
        fi
    else
        print_status "ERROR" "$script_path not found"
        return 1
    fi
}

# Main verification sequence
main() {
    echo "=== Cart EJB Application - Complete Verification ==="
    echo "Starting comprehensive verification of Cart EJB deployment..."
    echo

    # Initialize counters
    local total_checks=0
    local passed_checks=0
    local failed_checks=0
    local warning_checks=0

    # Check 1: GlassFish Status
    total_checks=$((total_checks + 1))
    if run_check "check-glassfish-status.sh" "GlassFish Server Status"; then
        passed_checks=$((passed_checks + 1))
    else
        failed_checks=$((failed_checks + 1))
        print_status "ERROR" "GlassFish is not running properly. Cannot continue with other checks."
        exit 1
    fi

    # Check 2: Deployed Applications
    total_checks=$((total_checks + 1))
    if run_check "list-applications.sh" "Deployed Applications"; then
        passed_checks=$((passed_checks + 1))
    else
        failed_checks=$((failed_checks + 1))
    fi

    # Check 3: EJB Container
    total_checks=$((total_checks + 1))
    if run_check "check-ejb-container.sh" "EJB Container Status"; then
        passed_checks=$((passed_checks + 1))
    else
        failed_checks=$((failed_checks + 1))
    fi

    # Check 4: JNDI Bindings
    total_checks=$((total_checks + 1))
    if run_check "check-ejb-jndi.sh" "EJB JNDI Bindings"; then
        passed_checks=$((passed_checks + 1))
    else
        failed_checks=$((failed_checks + 1))
    fi

    # Check 5: Security Configuration
    total_checks=$((total_checks + 1))
    if run_check "check-security-config.sh" "Security Configuration"; then
        passed_checks=$((passed_checks + 1))
    else
        # Security check failure is often a warning, not a critical error
        warning_checks=$((warning_checks + 1))
        print_status "WARNING" "Security configuration check had issues, but may not prevent EJB operation"
    fi

    echo
    echo "=========================================="
    echo "VERIFICATION SUMMARY"
    echo "=========================================="

    echo "Total checks run: $total_checks"
    print_status "SUCCESS" "Passed: $passed_checks"

    if [ $failed_checks -gt 0 ]; then
        print_status "ERROR" "Failed: $failed_checks"
    fi

    if [ $warning_checks -gt 0 ]; then
        print_status "WARNING" "Warnings: $warning_checks"
    fi

    # Overall assessment
    echo
    if [ $failed_checks -eq 0 ]; then
        if [ $warning_checks -eq 0 ]; then
            print_status "SUCCESS" "ALL CHECKS PASSED - Cart EJB is fully operational"
            echo
            echo "=== DEPLOYMENT STATUS ==="
            print_status "SUCCESS" "Cart EJB application is successfully deployed and ready for use"
            print_status "SUCCESS" "All system components are functioning correctly"
            echo
            echo "=== NEXT STEPS ==="
            echo "• Create EJB client applications to interact with the Cart service"
            echo "• Use JNDI lookup to access the CartBean"
            echo "• Ensure clients have proper security credentials (TutorialUser role)"
            echo "• Test cart operations: initialize, addBook, removeBook, getContents, remove"
        else
            print_status "WARNING" "MOSTLY OPERATIONAL - Cart EJB is deployed but has configuration warnings"
            echo
            echo "=== DEPLOYMENT STATUS ==="
            print_status "SUCCESS" "Cart EJB application is deployed and should work"
            print_status "WARNING" "Some configuration issues detected - review warnings above"
            echo
            echo "=== RECOMMENDED ACTIONS ==="
            echo "• Review security configuration warnings"
            echo "• Test basic EJB functionality to ensure it works despite warnings"
            echo "• Consider fixing configuration issues for production deployment"
        fi
        exit 0
    else
        print_status "ERROR" "VERIFICATION FAILED - Cart EJB has deployment issues"
        echo
        echo "=== DEPLOYMENT STATUS ==="
        print_status "ERROR" "Cart EJB application has critical issues"
        print_status "ERROR" "$failed_checks critical check(s) failed"
        echo
        echo "=== REQUIRED ACTIONS ==="
        echo "• Fix the failed checks listed above"
        echo "• Ensure GlassFish is running properly"
        echo "• Verify application deployment succeeded"
        echo "• Check GlassFish logs for detailed error information"
        echo "• Re-run this script after fixing issues"
        exit 1
    fi
}

# Function to show usage
show_usage() {
    echo "Cart EJB Application - Master Verification Script"
    echo
    echo "Usage: $0 [options]"
    echo
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -v, --verbose  Enable verbose output"
    echo
    echo "This script runs comprehensive verification of:"
    echo "  • GlassFish server status"
    echo "  • Deployed applications"
    echo "  • EJB container status"
    echo "  • JNDI bindings"
    echo "  • Security configuration"
    echo
    echo "Prerequisites:"
    echo "  • Must be run inside GlassFish container"
    echo "  • All verification scripts must be present in same directory"
    echo "  • Scripts must be executable (chmod +x *.sh)"
    echo
    echo "Individual verification scripts:"
    echo "  • check-glassfish-status.sh"
    echo "  • list-applications.sh"
    echo "  • check-ejb-container.sh"
    echo "  • check-ejb-jndi.sh"
    echo "  • check-security-config.sh"
}

# Check for help flag
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_usage
    exit 0
fi

# Check if running in verbose mode
if [ "$1" = "-v" ] || [ "$1" = "--verbose" ]; then
    set -x
fi

# Check if we're likely running in the correct environment
if ! command -v asadmin &> /dev/null; then
    print_status "ERROR" "asadmin command not found"
    echo "This script must be run inside the GlassFish container"
    echo
    echo "To run from outside the container:"
    echo "  docker-compose exec -T glassfish /tmp/verify-all.sh"
    echo
    echo "To run from inside the container:"
    echo "  docker-compose exec glassfish bash"
    echo "  # then run: /tmp/verify-all.sh"
    exit 1
fi

# Run main verification
main "$@"
