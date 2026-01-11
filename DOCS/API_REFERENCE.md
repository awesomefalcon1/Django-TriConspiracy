# Django API Reference

## Base URL

All API endpoints are prefixed with `/api/`

Example: `http://your-onion-address.onion/api/health/`

## API Root

**GET** `/api/`

Returns information about the API and available endpoints.

**Response:**
```json
{
  "name": "TriConspiracy API",
  "version": "1.0",
  "description": "Pure API backend - Frontend is handled by Vite-Crashout",
  "endpoints": {
    "health": "/api/health/",
    "health_simple": "/api/health/simple/",
    "auth": {...},
    "blog": {...},
    "chat": {...},
    "dh": {...}
  }
}
```

## Health Check Endpoints

### Detailed Health Check
**GET** `/api/health/`

Returns detailed server, database, and API status.

**Response:**
```json
{
  "status": "healthy" | "degraded" | "unhealthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "server": {
    "django_version": "5.1.3",
    "python_version": "3.11.0",
    "platform": "Linux-..."
  },
  "database": {
    "status": "connected",
    "connected": true,
    "counts": {
      "blog_posts": 10,
      "chat_messages": 25,
      "users": 5,
      "categories": 3
    }
  },
  "api": {
    "endpoints_available": true,
    "cors_enabled": true
  },
  "services": {
    "cache": "available"
  }
}
```

### Simple Health Check
**GET** `/api/health/simple/`

Returns simple OK status.

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Authentication Endpoints

### Get Challenge
**GET** `/api/cors/challenge/`

Get authentication challenge string.

**Response:**
```json
{
  "challenge": "random_challenge_string"
}
```

### Register User
**POST** `/api/cors/register/`

Register a new user with public key.

**Request:**
```json
{
  "public_key": "-----BEGIN PUBLIC KEY-----\n..."
}
```

**Response:**
```json
{
  "success": true,
  "message": "User created successfully",
  "fingerprint": "abc123...",
  "user_id": 1
}
```

### Login
**POST** `/api/cors/login/`

Authenticate user with signature.

**Request:**
```json
{
  "public_key": "-----BEGIN PUBLIC KEY-----\n...",
  "challenge": "challenge_string",
  "signature": "base64_signature"
}
```

**Response:**
```json
{
  "success": true,
  "user": {
    "fingerprint": "abc123...",
    "user_id": 1
  },
  "message": "Authentication successful"
}
```

## Blog Endpoints

### Get Posts
**GET** `/api/cors/posts/`

Get list of published blog posts.

**Response:**
```json
{
  "posts": [
    {
      "id": 1,
      "title": "Post Title",
      "slug": "post-title",
      "excerpt": "Post excerpt...",
      "author": "abc123",
      "author_fingerprint": "abc123...",
      "created_at": "2024-01-01T12:00:00Z",
      "category": "Technology"
    }
  ]
}
```

### Create Post
**POST** `/api/cors/posts/create/`

Create a new blog post (requires authentication).

**Request:**
```json
{
  "public_key": "-----BEGIN PUBLIC KEY-----\n...",
  "challenge": "challenge_string",
  "signature": "base64_signature",
  "title": "Post Title",
  "content": "Post content...",
  "excerpt": "Post excerpt (optional)",
  "category": "Technology (optional)",
  "published": true,
  "tags": ["tag1", "tag2"]
}
```

**Response:**
```json
{
  "success": true,
  "post": {
    "id": 1,
    "title": "Post Title",
    "slug": "post-title",
    "url": "/post/post-title/"
  }
}
```

## Chat Endpoints

### Get Messages
**GET** `/api/cors/chat/messages/?limit=50`

Get recent chat messages.

**Response:**
```json
{
  "messages": [
    {
      "id": 1,
      "sender": "abc123",
      "content": "Message content",
      "created_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

### Send Message
**POST** `/api/cors/chat/send/`

Send a chat message (authentication optional).

**Request:**
```json
{
  "content": "Message content",
  "public_key": "-----BEGIN PUBLIC KEY-----\n... (optional)",
  "challenge": "challenge_string (optional)",
  "signature": "base64_signature (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "message": {
    "id": 1,
    "sender": "abc123",
    "content": "Message content",
    "created_at": "2024-01-01T12:00:00Z"
  }
}
```

## Diffie-Hellman Endpoints

### Initialize Session
**POST** `/api/dh/initialize/`

Initialize a Diffie-Hellman session.

**Request:**
```json
{
  "session_id": "optional_session_id",
  "peer_public_key": "base64_encoded_public_key (optional)"
}
```

**Response:**
```json
{
  "success": true,
  "public_key": "base64_encoded_public_key",
  "session_id": "session_id"
}
```

### Send Encrypted Message
**POST** `/api/dh/send/`

Send an encrypted message using DH.

**Request:**
```json
{
  "session_id": "session_id",
  "message": "plaintext_message",
  "type": "chat" | "blog_post",
  "encrypted": {
    "dh": "...",
    "ct": "...",
    "mac": "...",
    "iv": "..."
  }
}
```

### Receive Encrypted Message
**POST** `/api/dh/receive/`

Receive and decrypt a message.

**Request:**
```json
{
  "session_id": "session_id",
  "encrypted": {
    "dh": "...",
    "ct": "...",
    "mac": "...",
    "iv": "..."
  }
}
```

**Response:**
```json
{
  "success": true,
  "message": "decrypted_message"
}
```

## Error Responses

All endpoints return errors in this format:

```json
{
  "error": "Error message description"
}
```

**Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error
- `503` - Service Unavailable (health check)

## CORS

All endpoints support CORS and can be called from the Vite-Crashout frontend.

## Authentication

Most endpoints support optional authentication via:
- Public key
- Challenge-response signature

Some endpoints (like creating posts) require authentication.

---

**Note:** This is a pure API backend. All frontend logic is in Vite-Crashout.
