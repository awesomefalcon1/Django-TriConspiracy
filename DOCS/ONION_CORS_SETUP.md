# Onion Service + CORS Setup Guide

## Overview

This setup allows the Vite-Crashout frontend (hosted anywhere) to connect to the Django-TriConspiracy backend via a Tor Onion Service.

## How It Works

1. **Frontend** (Vite-Crashout) - Hosted on Netlify/GitHub Pages/etc.
2. **Backend** (Django-TriConspiracy) - Running as Tor Hidden Service (.onion address)
3. **Browser** - Makes CORS requests from frontend URL to onion address

## Security Notes

- ✅ **Onion services use HTTP** (not HTTPS) - this is normal
- ✅ **Tor provides encryption** at the network layer
- ✅ **CORS_ALLOW_ALL_ORIGINS = True** is safe because:
  - Only requests through Tor can reach the onion service
  - The onion service itself is protected by Tor's network
  - CORS is for browser security, not network security

## Setup Steps

### 1. Configure Django CORS

The Django settings are already configured:
- `CORS_ALLOW_ALL_ORIGINS = True` - Allows browser requests from any origin
- `CORS_ALLOW_CREDENTIALS = True` - Allows cookies/auth headers
- All necessary HTTP methods and headers are allowed

### 2. Set Up Tor Hidden Service

If not already set up:

1. Install Tor on your server
2. Configure hidden service in `/etc/tor/torrc`:
   ```
   HiddenServiceDir /var/lib/tor/django_hidden_service/
   HiddenServicePort 80 127.0.0.1:8000
   ```
3. Restart Tor: `sudo systemctl restart tor`
4. Get your onion address: `sudo cat /var/lib/tor/django_hidden_service/hostname`

### 3. Configure Frontend Environment Variable

In Vite-Crashout, set the environment variable:

**For Netlify:**
1. Go to Site settings → Build & deploy → Environment variables
2. Add: `VITE_API_BASE_URL = http://your-onion-address.onion`

**For Local Development:**
Create `.env` file in Vite-Crashout:
```
VITE_API_BASE_URL=http://your-onion-address.onion
```

**For GitHub Pages:**
Set in repository settings → Secrets → Actions (if using GitHub Actions)
Or use a build script that sets the variable

### 4. Access the Frontend

1. **User must use Tor Browser** to access the frontend
2. Frontend loads from Netlify/GitHub Pages/etc.
3. Frontend makes API calls to the onion address
4. Tor Browser routes requests through Tor network
5. Django receives requests and responds (CORS allows it)

## Testing

### Test CORS from Browser Console

Open browser console on your frontend and run:

```javascript
fetch('http://your-onion-address.onion/api/dh/blog/posts/', {
  method: 'GET',
  credentials: 'include',
  headers: {
    'Content-Type': 'application/json',
  }
})
.then(r => r.json())
.then(data => console.log('Success:', data))
.catch(err => console.error('Error:', err));
```

### Expected Behavior

- ✅ Request succeeds (if Tor Browser is used)
- ✅ CORS headers are present in response
- ✅ Data is returned

### Common Issues

**CORS Error:**
- Make sure `CORS_ALLOW_ALL_ORIGINS = True` in Django settings
- Check that `corsheaders` middleware is enabled
- Verify Django server is running

**Connection Refused:**
- Tor Browser must be running
- Onion service must be configured correctly
- Django must be listening on the correct port

**Network Error:**
- Check onion address is correct
- Verify Tor is routing correctly
- Check Django logs for errors

## API Endpoints

The frontend uses these endpoints:

### Chat
- `GET /api/dh/chat/messages/` - Get chat messages
- `POST /api/cors/chat/send/` - Send chat message

### Blog
- `GET /api/dh/blog/posts/` - Get blog posts
- `POST /api/cors/posts/create/` - Create blog post

## Production Considerations

1. **Rate Limiting**: Consider adding rate limiting to prevent abuse
2. **Monitoring**: Monitor CORS requests and onion service access
3. **Error Handling**: Frontend should handle connection errors gracefully
4. **User Instructions**: Inform users they need Tor Browser

## Troubleshooting

### Django CORS Not Working

Check:
1. `corsheaders` is in `INSTALLED_APPS`
2. `CorsMiddleware` is in `MIDDLEWARE` (before CommonMiddleware)
3. `CORS_ALLOW_ALL_ORIGINS = True` is set
4. Django server is accessible via onion address

### Frontend Can't Connect

Check:
1. Environment variable `VITE_API_BASE_URL` is set correctly
2. Tor Browser is running
3. Onion address is correct
4. Network tab shows the request (even if it fails)

### Browser Console Errors

- **CORS error**: Django CORS not configured correctly
- **Network error**: Tor/onion service issue
- **404 error**: API endpoint doesn't exist
- **500 error**: Django server error (check logs)

## Security Best Practices

1. ✅ Use Tor Browser for accessing onion services
2. ✅ Keep Django and dependencies updated
3. ✅ Monitor for suspicious activity
4. ✅ Use strong authentication (public key auth)
5. ✅ Encrypt sensitive data (DH encryption)

## Summary

- Frontend: Any hosting (Netlify, GitHub Pages, etc.)
- Backend: Tor Hidden Service (.onion)
- Connection: Browser → Frontend → Onion Address (via Tor)
- CORS: Enabled for all origins (safe with Tor protection)

The setup is complete and ready to use!
