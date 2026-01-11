#!/bin/bash
# Script to configure Tor hidden service for Django

# Configuration
HIDDEN_SERVICE_DIR="/var/lib/tor/django_hidden_service"
DJANGO_PORT="8000"
TORRC_FILE="/etc/tor/torrc"

echo "Configuring Tor hidden service for Django..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo: sudo bash setup_tor.sh"
    exit 1
fi

# Create hidden service directory
echo "Creating hidden service directory: $HIDDEN_SERVICE_DIR"
mkdir -p "$HIDDEN_SERVICE_DIR"
chown debian-tor:debian-tor "$HIDDEN_SERVICE_DIR"
chmod 700 "$HIDDEN_SERVICE_DIR"

# Check if hidden service is already configured
if grep -q "HiddenServiceDir.*django_hidden_service" "$TORRC_FILE"; then
    echo "Hidden service for Django already configured in $TORRC_FILE"
    echo "Removing old configuration..."
    sed -i '/HiddenServiceDir.*django_hidden_service/,/^$/d' "$TORRC_FILE"
fi

# Add hidden service configuration
echo "" >> "$TORRC_FILE"
echo "## Django Hidden Service Configuration" >> "$TORRC_FILE"
echo "HiddenServiceDir $HIDDEN_SERVICE_DIR" >> "$TORRC_FILE"
echo "HiddenServicePort 80 127.0.0.1:$DJANGO_PORT" >> "$TORRC_FILE"

echo "Configuration added to $TORRC_FILE"
echo ""
echo "Restarting Tor service..."
systemctl restart tor

# Wait a moment for Tor to start
sleep 3

# Check if Tor is running
if systemctl is-active --quiet tor; then
    echo "✓ Tor service is running"
    
    # Get the .onion address
    if [ -f "$HIDDEN_SERVICE_DIR/hostname" ]; then
        echo ""
        echo "✓ Hidden service configured successfully!"
        echo "Your Django site is accessible at:"
        cat "$HIDDEN_SERVICE_DIR/hostname"
        echo ""
        echo "Make sure Django is running on port $DJANGO_PORT"
    else
        echo "⚠ Hidden service directory created, but hostname not yet generated."
        echo "   It may take a few moments. Check with: sudo cat $HIDDEN_SERVICE_DIR/hostname"
    fi
else
    echo "✗ Tor service failed to start. Check logs with: sudo journalctl -u tor"
    exit 1
fi
