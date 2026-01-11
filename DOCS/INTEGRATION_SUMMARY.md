# TriConspiracy - Vite UI + Django Backend Integration

## Overview

This integration connects the Django-TriConspiracy-Vite React UI with the Django backend using Diffie-Hellman key exchange (based on q3.py from CS459HW2).

## Architecture

### Frontend (React + Vite)
- **Location:** `Django-TriConspiracy-Vite/`
- **Framework:** React + TypeScript + Material-UI
- **Pages:**
  - HomePage (Landing)
  - BlogPage (Blog posts with DH encryption)
  - ChatPage (Chat messages with DH encryption)

### Backend (Django)
- **Location:** `Django-TriConspiracy/`
- **DH Module:** `blog/dh_communication.py` (based on q3.py)
- **API Endpoints:** `blog/dh_views.py`
- **URLs:** Added DH endpoints to `blog/urls.py`

## Diffie-Hellman Implementation

### Backend (Python)
Uses `cryptography` library with traditional DH:
- 2048-bit parameters
- AES-CBC encryption
- HMAC-SHA256 for message authentication
- Forward secrecy (new key pair per message)

### Frontend (JavaScript/TypeScript)
**Note:** Web Crypto API doesn't support traditional DH directly. Options:

1. **Use a library** (Recommended):
   - `node-forge` - Full DH support
   - `asmCrypto` - Cryptographic primitives
   - `crypto-js` - Various algorithms

2. **Current Implementation:**
   - Uses ECDH (Elliptic Curve DH) as a placeholder
   - **Needs to be updated** to use traditional DH with a library

## Setup Instructions

### 1. Backend Setup

```bash
cd Django-TriConspiracy
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 2. Frontend Setup

```bash
cd Django-TriConspiracy-Vite
npm install

# Install DH library (choose one):
npm install node-forge
# OR
npm install asmcrypto.js

# Development
npm run dev

# Build for production
npm run build
```

### 3. Environment Variables

Create `.env` in `Django-TriConspiracy-Vite/`:
```
VITE_API_BASE_URL=http://localhost:8000
# For production with Tor:
# VITE_API_BASE_URL=http://your-onion-address.onion
```

### 4. Update DH API Service

The `src/services/dhApi.ts` currently uses ECDH. Update it to use traditional DH:

```typescript
// Example with node-forge:
import forge from 'node-forge';

// Generate DH parameters and keys
const dh = forge.pki.dh.generateKeyPair(2048);
// ... implement DH key exchange
```

## API Endpoints

### DH Initialization
- `POST /api/dh/initialize/`
- Body: `{ "session_id": "...", "peer_public_key": "..." }`
- Returns: `{ "public_key": "...", "session_id": "..." }`

### Send Encrypted Message
- `POST /api/dh/send/`
- Body: `{ "session_id": "...", "message": "...", "type": "chat|blog_post", "encrypted": {...} }`
- Returns: `{ "success": true, "encrypted": {...} }`

### Receive Encrypted Message
- `POST /api/dh/receive/`
- Body: `{ "session_id": "...", "encrypted": {...} }`
- Returns: `{ "success": true, "message": "..." }`

### Chat Messages
- `GET /api/dh/chat/messages/?limit=50`
- Returns: `{ "messages": [...] }`

### Blog Posts
- `GET /api/dh/blog/posts/`
- Returns: `{ "posts": [...] }`

### Create Blog Post
- `POST /api/dh/blog/create/`
- Body: `{ "session_id": "...", "encrypted": {...} }`
- Encrypted message contains: `{ "title": "...", "content": "...", ... }`

## Features

### Blog
- ✅ View published posts
- ✅ Create new posts (encrypted via DH)
- ✅ Categories and tags
- ✅ Cyberpunk-themed UI

### Chat
- ✅ Real-time messaging (5s auto-refresh)
- ✅ Encrypted messages via DH
- ✅ Anonymous or authenticated
- ✅ Modern chat interface

## Security Features

1. **Diffie-Hellman Key Exchange**
   - Forward secrecy (new keys per message)
   - 2048-bit parameters
   - Secure key derivation (HKDF)

2. **Message Encryption**
   - AES-CBC with random IV
   - HMAC-SHA256 for authentication
   - Prevents tampering

3. **Tor Integration**
   - Works with .onion addresses
   - Network-layer encryption
   - CORS configured for GitHub/GitLab Pages

## Known Issues & TODO

1. **Frontend DH Implementation**
   - Currently uses ECDH (placeholder)
   - Needs traditional DH library (node-forge recommended)
   - Update `src/services/dhApi.ts`

2. **Session Management**
   - Currently in-memory (`_dh_sessions` dict)
   - Should use Redis or database for production

3. **Error Handling**
   - Add retry logic
   - Better error messages
   - Connection status indicators

4. **Performance**
   - Optimize key derivation
   - Cache shared secrets
   - Batch message operations

## Development Notes

### Running Both Servers

**Terminal 1 (Django):**
```bash
cd Django-TriConspiracy
python manage.py runserver
```

**Terminal 2 (Vite):**
```bash
cd Django-TriConspiracy-Vite
npm run dev
```

Access:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000

### Building for Production

1. Build Vite app:
```bash
cd Django-TriConspiracy-Vite
npm run build
```

2. Serve from Django (optional):
   - Copy `dist/` to Django static files
   - Or serve separately (recommended for GitHub Pages)

3. Configure CORS:
   - Add your frontend URL to `CORS_ALLOWED_ORIGINS` in `main/settings.py`

## Testing

1. **Initialize DH Session:**
   - Frontend automatically initializes on first API call
   - Check browser console for errors

2. **Send Message:**
   - Type in chat and send
   - Verify encryption/decryption works

3. **Create Blog Post:**
   - Fill form and submit
   - Verify post appears in list

## Troubleshooting

### CORS Errors
- Check `CORS_ALLOWED_ORIGINS` in Django settings
- Verify frontend URL matches allowed origins
- Check browser console for specific errors

### DH Key Exchange Fails
- Verify backend DH module is working
- Check session_id is consistent
- Ensure keys are properly serialized/deserialized

### Messages Not Appearing
- Check backend logs for errors
- Verify database migrations ran
- Check API endpoint responses

## Next Steps

1. Implement proper DH in frontend (node-forge)
2. Add user authentication (optional)
3. Implement message persistence
4. Add real-time updates (WebSockets)
5. Deploy to production
