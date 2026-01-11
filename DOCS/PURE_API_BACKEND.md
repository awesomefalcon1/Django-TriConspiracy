# Django Pure API Backend

## Overview

Django has been refactored into a **pure API backend** with no frontend logic. All frontend is handled by **Vite-Crashout**.

## What Was Removed

### ❌ Removed Template Views
- `post_list()` - Removed (use `/api/cors/posts/` instead)
- `post_detail()` - Removed (frontend handles display)
- `category_detail()` - Removed (frontend handles filtering)
- `login_page()` - Removed (frontend handles login UI)
- `user_profile()` - Removed (frontend handles profiles)
- `post_create()` - Removed (use `/api/cors/posts/create/` instead)
- `auth_logout()` - Removed (frontend handles logout)

### ❌ Removed Template URLs
- `/` - Removed (now returns API info at `/api/`)
- `/post/<slug>/` - Removed
- `/create/` - Removed
- `/category/<slug>/` - Removed
- `/profile/` - Removed
- `/login/` - Removed
- `/logout/` - Removed

### ✅ Kept (API Only)
- All `/api/*` endpoints
- `/admin/` - Django admin interface (backend management only)

## Current API Structure

### Health Check
- `GET /api/health/` - Detailed health check
- `GET /api/health/simple/` - Simple health check

### Authentication
- `GET /api/cors/challenge/` - Get authentication challenge
- `POST /api/cors/register/` - Register with public key
- `POST /api/cors/login/` - Authenticate with signature

### Blog
- `GET /api/cors/posts/` - Get published posts
- `POST /api/cors/posts/create/` - Create blog post

### Chat
- `GET /api/cors/chat/messages/` - Get chat messages
- `POST /api/cors/chat/send/` - Send chat message

### Diffie-Hellman
- `POST /api/dh/initialize/` - Initialize DH session
- `POST /api/dh/send/` - Send encrypted message
- `POST /api/dh/receive/` - Receive encrypted message
- `GET /api/dh/chat/messages/` - Get chat messages
- `GET /api/dh/blog/posts/` - Get blog posts
- `POST /api/dh/blog/create/` - Create encrypted blog post

### API Root
- `GET /api/` - Returns API information and available endpoints

## Files Structure

### New Files
- `blog/api_views.py` - All API views (pure JSON responses)

### Modified Files
- `blog/urls.py` - Only API endpoints, no template routes
- `main/urls.py` - Added API root endpoint
- `main/settings.py` - Noted that templates are only for admin

### Old Files (Can be removed)
- `blog/views.py` - Contains old template views (kept for reference, not used)
- `blog/templates/` - Template files (not used, kept for admin if needed)

## API Response Format

All endpoints return JSON:

```json
{
  "success": true,
  "data": {...},
  "error": null
}
```

Or for errors:

```json
{
  "error": "Error message",
  "success": false
}
```

## Frontend Integration

The Vite-Crashout frontend:
- ✅ Makes API calls to Django backend
- ✅ Handles all UI/UX
- ✅ Manages routing
- ✅ Displays data
- ✅ Handles user interactions

Django backend:
- ✅ Only returns JSON
- ✅ No HTML rendering
- ✅ No template logic
- ✅ Pure API responses

## Testing

### Test API Root

```bash
curl http://your-onion-address.onion/api/
```

Returns:
```json
{
  "name": "TriConspiracy API",
  "version": "1.0",
  "description": "Pure API backend - Frontend is handled by Vite-Crashout",
  "endpoints": {...}
}
```

### Test Health Check

```bash
curl http://your-onion-address.onion/api/health/
```

### Test from Frontend

The Vite-Crashout frontend automatically uses these endpoints via the `api` service.

## Migration Notes

If you had bookmarks or links to old Django pages:
- `/` → Use frontend at Vite-Crashout
- `/post/<slug>/` → Frontend handles routing
- `/login/` → Frontend handles login UI
- All functionality moved to API endpoints

## Admin Interface

The Django admin interface (`/admin/`) is still available for:
- Backend management
- Database administration
- User management
- Content moderation

This is separate from the API and requires admin authentication.

## Benefits

1. ✅ **Separation of Concerns** - Frontend and backend are completely separate
2. ✅ **Scalability** - Frontend and backend can be scaled independently
3. ✅ **Flexibility** - Frontend can be updated without touching backend
4. ✅ **API-First** - Clean REST API design
5. ✅ **CORS Ready** - All endpoints support CORS for frontend access

## Summary

- ✅ Django is now a **pure API backend**
- ✅ All frontend logic moved to **Vite-Crashout**
- ✅ All endpoints return **JSON only**
- ✅ No templates, no HTML rendering (except admin)
- ✅ Clean API structure

---

**Status:** ✅ Django is now a pure API backend!
