#!/bin/bash
# Deployment script for FMWA Website

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to display error messages
error() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

# Function to display success messages
success() {
    echo -e "${GREEN}$1${NC}"
}

# Function to display info messages
info() {
    echo -e "${YELLOW}$1${NC}"
}

# Check if the script is run as root
if [ "$(id -u)" -eq 0 ]; then
    error "This script should not be run as root. Please run as a normal user with sudo privileges."
fi

# Check for required commands
for cmd in rsync ssh sshpass; do
    if ! command -v $cmd &> /dev/null; then
        error "$cmd is required but not installed. Please install it first."
    fi
done

# Load deployment configuration
if [ ! -f ".deployment" ]; then
    error "Deployment configuration file (.deployment) not found!"
fi

# Source the deployment configuration
# shellcheck source=/dev/null
source .deployment

# Function to upload files
upload_files() {
    local remote_host="$1"
    local remote_user="$2"
    local remote_path="$3"
    local ssh_port="${4:-22}"
    
    info "Starting file upload to $remote_user@$remote_host:$remote_path..."
    
    # Create exclude list for rsync
    echo "Creating exclude list..."
    echo ".git/" > /tmp/rsync_exclude
    echo "node_modules/" >> /tmp/rsync_exclude
    echo ".env" >> /tmp/rsync_exclude
    echo "*.log" >> /tmp/rsync_exclude
    echo "*.sql" >> /tmp/rsync_exclude
    
    # Upload files using rsync
    rsync -avz --delete \
        --exclude-from=/tmp/rsync_exclude \
        -e "ssh -p $ssh_port" \
        . "$remote_user@$remote_host:$remote_path/" || error "File upload failed"
    
    rm /tmp/rsync_exclude
    success "Files uploaded successfully!"
}

# Function to set permissions
set_permissions() {
    local remote_host="$1"
    local remote_user="$2"
    local remote_path="$3"
    local ssh_port="${4:-22}"
    
    info "Setting file permissions..."
    
    # Set directory permissions
    ssh -p "$ssh_port" "$remote_user@$remote_host" "
        cd '$remote_path' && \
        find . -type d -exec chmod 755 {} \; && \
        find . -type f -exec chmod 644 {} \; && \
        chmod -R 775 storage/ bootstrap/cache/ && \
        chmod 775 database/database.sqlite || exit 1
    " || error "Failed to set permissions"
    
    success "Permissions set successfully!"
}

# Function to run deployment commands
run_deployment_commands() {
    local remote_host="$1"
    local remote_user="$2"
    local remote_path="$3"
    local ssh_port="${4:-22}"
    
    info "Running deployment commands..."
    
    # Run composer install
    ssh -p "$ssh_port" "$remote_user@$remote_host" "
        cd '$remote_path' && \
        composer install --no-dev --optimize-autoloader && \
        php artisan config:cache && \
        php artisan route:cache && \
        php artisan view:cache
    " || error "Deployment commands failed"
    
    success "Deployment completed successfully!"
}

# Main deployment function
deploy() {
    local remote_host=""
    local remote_user=""
    local remote_path=""
    local ssh_port="22"
    
    # Get deployment settings
    read -p "Enter remote host (e.g., example.com): " remote_host
    read -p "Enter SSH username: " remote_user
    read -p "Enter remote path (e.g., /var/www/fmwa): " remote_path
    read -p "Enter SSH port [22]: " ssh_port
    ssh_port="${ssh_port:-22}"
    
    # Upload files
    upload_files "$remote_host" "$remote_user" "$remote_path" "$ssh_port"
    
    # Set permissions
    set_permissions "$remote_host" "$remote_user" "$remote_path" "$ssh_port"
    
    # Run deployment commands
    run_deployment_commands "$remote_host" "$remote_user" "$remote_path" "$ssh_port"
    
    success "\n🎉 Deployment completed successfully!"
    info "Your application should now be live at: http://$remote_host/"
}

# Run deployment
echo -e "\n${YELLOW}🚀 FMWA Website Deployment Script${NC}\n"
deploy
