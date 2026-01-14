#!/bin/bash

# Interactive menu for Cart EJB verification scripts
# Usage: ./interactive-menu.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_header() {
    echo -e "${CYAN}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Function to check if we're in container
check_environment() {
    if command -v asadmin &> /dev/null; then
        return 0  # Inside container
    else
        return 1  # Outside container
    fi
}

# Function to run script based on environment
run_script() {
    local script_name=$1

    if check_environment; then
        # Inside container
        if [ -x "/tmp/$script_name" ]; then
            /tmp/$script_name
        else
            print_error "Script /tmp/$script_name not found or not executable"
            echo "Run the setup first: just setup-scripts"
            return 1
        fi
    else
        # Outside container - use docker-compose
        if [ -f "docker-compose.yml" ]; then
            docker-compose exec -T glassfish /tmp/$script_name
        else
            print_error "docker-compose.yml not found"
            echo "Please run this from the project root directory"
            return 1
        fi
    fi
}

# Function to show main menu
show_menu() {
    clear
    print_header "========================================================"
    print_header "    Cart EJB Application - Verification Menu"
    print_header "========================================================"
    echo

    if check_environment; then
        print_info "Environment: Running inside GlassFish container"
    else
        print_info "Environment: Running outside container (using docker-compose)"
    fi

    echo
    echo "Choose an option:"
    echo
    echo "  ${GREEN}COMPLETE VERIFICATION${NC}"
    echo "  1) Run all verification checks"
    echo
    echo "  ${YELLOW}INDIVIDUAL CHECKS${NC}"
    echo "  2) Check GlassFish server status"
    echo "  3) List deployed applications"
    echo "  4) Check EJB container status"
    echo "  5) Check EJB JNDI bindings"
    echo "  6) Check security configuration"
    echo
    echo "  ${BLUE}INFORMATION${NC}"
    echo "  7) Show EJB connection info"
    echo "  8) Show help and usage instructions"
    echo
    echo "  ${CYAN}UTILITIES${NC}"
    echo "  9) Show container logs (last 20 lines)"
    echo " 10) Interactive shell (container only)"
    echo
    echo "  0) Exit"
    echo
    echo -n "Enter your choice [0-10]: "
}

# Function to show EJB connection info
show_connection_info() {
    clear
    print_header "========================================================"
    print_header "    Cart EJB Connection Information"
    print_header "========================================================"
    echo
    echo "JNDI Lookup Information:"
    echo "  Context: java:global/cart-secure-ejb-only/jakarta.examples.tutorial.security.cart-secure-cart-secure-ejb-10-SNAPSHOT/CartBean"
    echo "  Business Interface: jakarta.tutorial.cartsecure.ejb.Cart"
    echo "  Security Role: TutorialUser"
    echo
    echo "Connection Properties (for remote clients):"
    echo "  Initial Context Factory: com.sun.enterprise.naming.SerialInitContextFactory"
    echo "  Provider URL: iiop://localhost:3700"
    echo "  State Factories: com.sun.corba.ee.impl.presentation.rmi.JNDIStateFactoryImpl"
    echo
    echo "EJB Methods Available:"
    echo "  • initialize(String person)"
    echo "  • initialize(String person, String id)"
    echo "  • addBook(String title) [@RolesAllowed('TutorialUser')]"
    echo "  • removeBook(String title) [@RolesAllowed('TutorialUser')]"
    echo "  • getContents() [@RolesAllowed('TutorialUser')]"
    echo "  • remove() [@RolesAllowed('TutorialUser')]"
    echo
    echo "Example Client Code:"
    echo "  Properties props = new Properties();"
    echo "  props.setProperty(Context.INITIAL_CONTEXT_FACTORY,"
    echo "      \"com.sun.enterprise.naming.SerialInitContextFactory\");"
    echo "  props.setProperty(\"org.omg.CORBA.ORBInitialHost\", \"localhost\");"
    echo "  props.setProperty(\"org.omg.CORBA.ORBInitialPort\", \"3700\");"
    echo "  InitialContext ctx = new InitialContext(props);"
    echo "  Cart cart = (Cart) ctx.lookup(\"java:global/cart-secure-ejb-only/...\");"
    echo
}

# Function to show help
show_help() {
    clear
    print_header "========================================================"
    print_header "    Cart EJB Application - Help & Usage"
    print_header "========================================================"
    echo
    echo "About this application:"
    echo "  This is a Jakarta EE Enterprise Application that demonstrates"
    echo "  EJB security features using a shopping cart example."
    echo
    echo "Application Components:"
    echo "  • CartBean - Stateful session bean with business logic"
    echo "  • Security roles - @RolesAllowed('TutorialUser') on methods"
    echo "  • JNDI access - Remote EJB invocation via CORBA/IIOP"
    echo
    echo "Verification Scripts:"
    echo "  • check-glassfish-status.sh - Verify server is running"
    echo "  • list-applications.sh - Show deployed applications"
    echo "  • check-ejb-container.sh - Check EJB container status"
    echo "  • check-ejb-jndi.sh - Verify JNDI bindings"
    echo "  • check-security-config.sh - Check security settings"
    echo "  • verify-all.sh - Run complete verification"
    echo
    echo "External Commands (when outside container):"
    echo "  just setup-scripts    - Copy scripts to container"
    echo "  just verify          - Run complete verification"
    echo "  just verify-jndi     - Check JNDI bindings only"
    echo "  just list-apps       - List applications"
    echo "  just info            - Show application info"
    echo
    echo "Troubleshooting:"
    echo "  • Ensure container is running: docker-compose ps"
    echo "  • Check logs: docker-compose logs glassfish"
    echo "  • Verify deployment: just list-apps"
    echo "  • Check JNDI: just verify-jndi"
    echo
}

# Function to show logs
show_logs() {
    clear
    print_header "========================================================"
    print_header "    Container Logs (Last 20 lines)"
    print_header "========================================================"
    echo

    if check_environment; then
        print_warning "Cannot show container logs from inside the container"
        echo "To view logs from outside the container, run:"
        echo "  docker-compose logs --tail=20 glassfish"
    else
        if [ -f "docker-compose.yml" ]; then
            docker-compose logs --tail=20 glassfish
        else
            print_error "docker-compose.yml not found"
            echo "Please run this from the project root directory"
        fi
    fi
    echo
}

# Function to launch interactive shell
launch_shell() {
    if check_environment; then
        print_warning "Already running inside the container"
        echo "You can run verification scripts directly:"
        echo "  /tmp/verify-all.sh"
        echo "  /tmp/check-ejb-jndi.sh"
        echo "  etc."
    else
        if [ -f "docker-compose.yml" ]; then
            print_info "Launching interactive shell in GlassFish container..."
            echo "Once inside, you can run:"
            echo "  /tmp/verify-all.sh"
            echo "  /tmp/check-ejb-jndi.sh"
            echo "  asadmin list-applications"
            echo "  exit (to return to this menu)"
            echo
            echo "Press Enter to continue..."
            read
            docker-compose exec glassfish bash
        else
            print_error "docker-compose.yml not found"
            echo "Please run this from the project root directory"
        fi
    fi
}

# Function to pause and wait for user input
pause() {
    echo
    echo -n "Press Enter to continue..."
    read
}

# Main menu loop
main() {
    while true; do
        show_menu
        read choice

        case $choice in
            1)
                clear
                print_header "Running complete verification..."
                echo
                if run_script "verify-all.sh"; then
                    print_success "Complete verification finished"
                else
                    print_error "Verification failed or incomplete"
                fi
                pause
                ;;
            2)
                clear
                print_header "Checking GlassFish server status..."
                echo
                if run_script "check-glassfish-status.sh"; then
                    print_success "GlassFish status check completed"
                else
                    print_error "GlassFish status check failed"
                fi
                pause
                ;;
            3)
                clear
                print_header "Listing deployed applications..."
                echo
                if run_script "list-applications.sh"; then
                    print_success "Application list completed"
                else
                    print_error "Failed to list applications"
                fi
                pause
                ;;
            4)
                clear
                print_header "Checking EJB container status..."
                echo
                if run_script "check-ejb-container.sh"; then
                    print_success "EJB container check completed"
                else
                    print_error "EJB container check failed"
                fi
                pause
                ;;
            5)
                clear
                print_header "Checking EJB JNDI bindings..."
                echo
                if run_script "check-ejb-jndi.sh"; then
                    print_success "JNDI bindings check completed"
                else
                    print_error "JNDI bindings check failed"
                fi
                pause
                ;;
            6)
                clear
                print_header "Checking security configuration..."
                echo
                if run_script "check-security-config.sh"; then
                    print_success "Security configuration check completed"
                else
                    print_warning "Security configuration check completed with warnings"
                fi
                pause
                ;;
            7)
                show_connection_info
                pause
                ;;
            8)
                show_help
                pause
                ;;
            9)
                show_logs
                pause
                ;;
            10)
                launch_shell
                ;;
            0)
                clear
                print_success "Thank you for using Cart EJB verification tools!"
                echo "To run verification again, use:"
                if check_environment; then
                    echo "  /tmp/verify-all.sh"
                else
                    echo "  just verify"
                    echo "  ./scripts/interactive-menu.sh"
                fi
                echo
                exit 0
                ;;
            *)
                clear
                print_error "Invalid choice. Please select 0-10."
                echo
                pause
                ;;
        esac
    done
}

# Check if scripts are available
check_scripts() {
    if ! check_environment; then
        # Outside container - check if docker-compose is available
        if ! command -v docker-compose &> /dev/null; then
            print_error "docker-compose not found"
            echo "Please install Docker Compose to use this menu"
            exit 1
        fi

        if [ ! -f "docker-compose.yml" ]; then
            print_error "docker-compose.yml not found"
            echo "Please run this from the project root directory"
            exit 1
        fi

        # Check if container is running
        if ! docker-compose ps -q glassfish &>/dev/null; then
            print_error "GlassFish container is not running"
            echo "Please start the container first:"
            echo "  docker-compose up -d"
            exit 1
        fi
    fi

    # Check if verification scripts are available
    local script_available=false
    if check_environment; then
        if [ -x "/tmp/verify-all.sh" ]; then
            script_available=true
        fi
    else
        # Test by trying to run a simple command
        if docker-compose exec -T glassfish test -x /tmp/verify-all.sh 2>/dev/null; then
            script_available=true
        fi
    fi

    if [ "$script_available" = false ]; then
        print_warning "Verification scripts not found in container"
        echo
        if check_environment; then
            echo "Scripts should be available at /tmp/verify-all.sh"
            echo "Ask administrator to run: just setup-scripts"
        else
            echo "Would you like to set up the scripts now? (y/n)"
            read -r setup_choice
            if [ "$setup_choice" = "y" ] || [ "$setup_choice" = "Y" ]; then
                echo "Setting up scripts..."
                if [ -x "scripts/setup-scripts.sh" ]; then
                    ./scripts/setup-scripts.sh
                    print_success "Scripts setup completed"
                    echo
                else
                    print_error "Setup script not found: scripts/setup-scripts.sh"
                    echo "Please run: just setup-scripts"
                    exit 1
                fi
            else
                echo "Please run: just setup-scripts"
                exit 1
            fi
        fi
    fi
}

# Initialize and run
echo "Initializing Cart EJB verification menu..."
check_scripts
main
