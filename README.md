# TriConspiracy - Django Blog with Tor Hidden Service

A Django blog application configured to run as a Tor hidden service, featuring public key authentication, encrypted messaging, and a modern Materialize CSS UI.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Set up Tor hidden service:**
   See [DOCS/TOR_SETUP_INSTRUCTIONS.md](DOCS/TOR_SETUP_INSTRUCTIONS.md)

4. **Run the server:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## Features

- **Blog Posts**: Create, view, and manage blog posts
- **Categories & Tags**: Organize posts by categories and tags
- **Public Key Authentication**: Secure authentication using RSA key pairs
- **Tor Hidden Service**: Runs as a .onion address for privacy
- **Encrypted Communication**: Tor network-layer encryption
- **Modern UI**: Materialize CSS design

## Documentation

📚 **All documentation is in the [DOCS](DOCS/) folder.**

See [DOCS/README.md](DOCS/README.md) for a complete index of all documentation files.

### Quick Links

- **[Setup Guide](DOCS/TOR_SETUP_INSTRUCTIONS.md)** - Set up Tor hidden service
- **[Security Guide](DOCS/SECURITY_AND_USAGE.md)** - Security best practices
- **[API Reference](DOCS/API_REFERENCE.md)** - Complete API documentation
- **[Tor Encryption](DOCS/TOR_ENCRYPTION_EXPLAINED.md)** - How Tor encryption works

## Project Structure

```
Django-TriConspiracy/
├── blog/              # Main blog application
├── main/              # Django project settings
├── DOCS/              # All documentation (see DOCS/README.md)
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

## Requirements

- Python 3.8+
- Django 5.1+
- Tor (for hidden service)
- See `requirements.txt` for full list

## License

[Add your license here]

---

**For complete documentation, see [DOCS/README.md](DOCS/README.md)**
