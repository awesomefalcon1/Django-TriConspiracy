# Tor Hidden Service Setup for Django

## Quick Setup Commands

Run these commands to configure Tor for your Django project:

```bash
# 1. Edit Tor configuration
sudo nano /etc/tor/torrc

# 2. Add these lines at the end of the file:
HiddenServiceDir /var/lib/tor/django_hidden_service
HiddenServicePort 80 127.0.0.1:8000

# 3. Save and exit (Ctrl+X, then Y, then Enter)

# 4. Create the hidden service directory
sudo mkdir -p /var/lib/tor/django_hidden_service
sudo chown debian-tor:debian-tor /var/lib/tor/django_hidden_service
sudo chmod 700 /var/lib/tor/django_hidden_service

# 5. Restart Tor service
sudo systemctl restart tor

# 6. Wait a few seconds, then get your .onion address
sudo cat /var/lib/tor/django_hidden_service/hostname
```

## What This Does

- **HiddenServiceDir**: Sets the directory where Tor stores your hidden service keys and hostname
- **HiddenServicePort 80 127.0.0.1:8000**: Maps Tor's port 80 to your Django server running on localhost:8000

## Accessing Your Site

Once configured, your Django site will be accessible via the .onion address shown in the hostname file.
Make sure Django is running on port 8000:

```bash
cd /home/darcy/Django-TriConspiracy
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000
```

Then access your site using the .onion address in a Tor browser.

## Notes

- Django settings have been updated to allow localhost connections (required for Tor forwarding)
- The hidden service will be accessible on port 80 via Tor (which forwards to your Django on port 8000)
- Keep your .onion address private and secure
