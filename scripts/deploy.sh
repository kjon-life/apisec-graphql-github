#!/bin/bash
set -e

# Configuration
APP_NAME="spacexdata"
APP_DIR="$HOME/apps/${APP_NAME}"
VENV_DIR="${APP_DIR}/.venv"
REPO_URL="git@github.com:kjon-life/apisec-graphql-qa.git"
SERVICE_FILE="/etc/systemd/system/${APP_NAME}.service"
NGINX_CONF="/etc/nginx/conf.d/${APP_NAME}.conf"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Create application directory
log "Creating application directory..."
mkdir -p "$APP_DIR"

# Clone/update repository
log "Cloning/updating repository..."
if [ -d "${APP_DIR}/.git" ]; then
    cd "$APP_DIR"
    git pull
else
    git clone "$REPO_URL" "$APP_DIR"
fi

# Set up virtual environment
log "Setting up virtual environment..."
cd "$APP_DIR"
uv venv
source "${VENV_DIR}/bin/activate"

# Install dependencies
log "Installing dependencies..."
uv pip install -r requirements.txt

# Create systemd service file (requires sudo)
log "Setting up systemd service..."
sudo tee "$SERVICE_FILE" > /dev/null << EOL
[Unit]
Description=SpaceX GraphQL API Service
After=network.target

[Service]
User=$USER
WorkingDirectory=${APP_DIR}
Environment=PATH=${VENV_DIR}/bin:$PATH
ExecStart=${VENV_DIR}/bin/uvicorn main:app --host 0.0.0.0 --port 9070
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Set up nginx configuration (requires sudo)
log "Setting up nginx configuration..."
sudo tee "$NGINX_CONF" > /dev/null << EOL
server {
    listen 80;
    server_name spacexdata.kjon.life;

    location / {
        proxy_pass http://localhost:9070;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOL

# Set proper permissions
log "Setting permissions..."
sudo chmod 644 "$SERVICE_FILE"
sudo chmod 644 "$NGINX_CONF"

# Reload systemd and restart services (requires sudo)
log "Reloading systemd and restarting services..."
sudo systemctl daemon-reload
sudo systemctl enable "$APP_NAME"
sudo systemctl restart "$APP_NAME"
sudo systemctl restart nginx

log "Deployment completed successfully!"
log "Next steps:"
log "1. Configure AWS security group to allow traffic on port 9070"
log "2. Set up SSL certificate with Let's Encrypt" 