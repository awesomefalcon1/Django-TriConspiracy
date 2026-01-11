# Username/Password Authentication

## Overview

Django backend now uses **standard username/password authentication** instead of public key authentication. This simplifies the authentication flow while maintaining security.

## Changes Made

### 1. User Model
- ✅ Removed `PublicKeyUser` custom model
- ✅ Using Django's default `User` model (username/password)
- ✅ Updated all foreign key references

### 2. Authentication Backend
- ✅ Removed `PublicKeyAuthBackend`
- ✅ Using Django's default `ModelBackend` (username/password)

### 3. API Endpoints

#### Register
**POST** `/api/cors/register/`

**Request:**
```json
{
  "username": "myusername",
  "password": "mypassword",
  "email": "user@example.com"  // optional
}
```

**Response:**
```json
{
  "success": true,
  "message": "User created successfully",
  "user": {
    "username": "myusername",
    "user_id": 1
  }
}
```

#### Login
**POST** `/api/cors/login/`

**Request:**
```json
{
  "username": "myusername",
  "password": "mypassword"
}
```

**Response:**
```json
{
  "success": true,
  "user": {
    "username": "myusername",
    "user_id": 1,
    "email": "user@example.com"
  },
  "message": "Authentication successful"
}
```

#### Logout
**POST** `/api/cors/logout/`

**Response:**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

### 4. Model Updates

#### BlogPost
- `author_user` now references `auth.User` instead of `PublicKeyUser`
- `author` field stores username instead of fingerprint

#### ChatMessage
- `sender` now references `auth.User` instead of `PublicKeyUser`
- `sender_username` field for anonymous messages (replaces `sender_fingerprint`)
- `get_sender_display()` returns username instead of fingerprint

### 5. Removed Endpoints
- ❌ `GET /api/cors/challenge/` - No longer needed (was for public key auth)

## Migration Notes

### Database Migration Required

You'll need to create and run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

**Important:** This will require data migration if you have existing users. The old `PublicKeyUser` model will be removed, so you may need to:

1. Export existing data
2. Create new User accounts
3. Migrate blog posts and chat messages to new User model

### For New Installations

If starting fresh, just run migrations normally.

## API Usage Examples

### Register New User

```javascript
const response = await fetch('http://your-onion-address.onion/api/cors/register/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include',
  body: JSON.stringify({
    username: 'myusername',
    password: 'mypassword',
    email: 'user@example.com'
  })
});

const data = await response.json();
```

### Login

```javascript
const response = await fetch('http://your-onion-address.onion/api/cors/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include',
  body: JSON.stringify({
    username: 'myusername',
    password: 'mypassword'
  })
});

const data = await response.json();
// Session cookie is automatically set
```

### Create Blog Post (Requires Authentication)

```javascript
// First login, then create post
const response = await fetch('http://your-onion-address.onion/api/cors/posts/create/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include',  // Include session cookie
  body: JSON.stringify({
    title: 'My Post',
    content: 'Post content...',
    excerpt: 'Post excerpt',
    published: true
  })
});
```

### Send Chat Message (Optional Authentication)

```javascript
// Authenticated message
const response = await fetch('http://your-onion-address.onion/api/cors/chat/send/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include',  // Include session cookie if logged in
  body: JSON.stringify({
    content: 'Hello, world!'
  })
});

// Anonymous message (no authentication)
const response = await fetch('http://your-onion-address.onion/api/cors/chat/send/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    content: 'Anonymous message',
    username: 'Anonymous'  // Optional display name
  })
});
```

## Security Notes

1. **Password Storage**: Django automatically hashes passwords using PBKDF2
2. **Session Management**: Uses Django's secure session framework
3. **CSRF Protection**: Enabled for state-changing operations
4. **CORS**: Configured to work with frontend on different domains

## Frontend Integration

The Vite-Crashout frontend should:

1. **Register/Login**: Use username/password forms
2. **Session Management**: Include `credentials: 'include'` in fetch requests
3. **Authentication State**: Check if user is logged in via session cookie
4. **Logout**: Call logout endpoint and clear session

## Benefits

1. ✅ **Simpler**: Standard username/password is more familiar
2. ✅ **Easier Integration**: Works with standard Django auth
3. ✅ **Better UX**: Users don't need to manage key pairs
4. ✅ **Still Secure**: Django's password hashing and session management
5. ✅ **DH Encryption**: Still available for message encryption (separate from auth)

## What Remains

- ✅ **Diffie-Hellman Encryption**: Still available for encrypted messages
- ✅ **CORS Support**: All endpoints support CORS
- ✅ **Health Checks**: Still available
- ✅ **Blog & Chat**: All functionality preserved

---

**Status:** ✅ Username/password authentication is now active!
