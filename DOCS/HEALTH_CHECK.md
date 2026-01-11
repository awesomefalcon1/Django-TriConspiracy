# Health Check System

## Overview

Health check endpoints have been added to monitor Django backend status and verify connectivity from the Vite frontend.

## Django Endpoints

### 1. Detailed Health Check
**Endpoint:** `GET /api/health/`

**Response:**
```json
{
  "status": "healthy" | "degraded" | "unhealthy",
  "timestamp": "2024-01-01T12:00:00Z",
  "server": {
    "django_version": "5.1.3",
    "python_version": "3.11.0",
    "platform": "Linux-6.14.0..."
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

**Status Codes:**
- `200` - Healthy
- `503` - Unhealthy or Degraded

### 2. Simple Health Check
**Endpoint:** `GET /api/health/simple/`

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**Status Code:** `200`

**Use Case:** Quick check for load balancers and simple monitoring

## Vite Frontend

### Health Check Component

A `HealthCheck` component has been added that:
- ✅ Displays server status (Healthy/Degraded/Unhealthy)
- ✅ Shows detailed information (expandable)
- ✅ Auto-refreshes every 30 seconds
- ✅ Manual refresh button
- ✅ Shows database connection status
- ✅ Displays model counts
- ✅ Shows API and CORS status

### Usage

The component is automatically included in:
- `BlogPage` - Shows at the top
- `ChatPage` - Shows at the top

### API Service Methods

```typescript
// Detailed health check
const health = await api.healthCheck();
console.log(health.status); // 'healthy' | 'degraded' | 'unhealthy'

// Simple health check
const simple = await api.healthCheckSimple();
console.log(simple.status); // 'ok'
```

## Testing

### Test from Browser Console

```javascript
// Test detailed health check
fetch('http://your-onion-address.onion/api/health/', {
  method: 'GET',
  credentials: 'include',
})
.then(r => r.json())
.then(data => console.log('Health:', data))
.catch(err => console.error('Error:', err));

// Test simple health check
fetch('http://your-onion-address.onion/api/health/simple/', {
  method: 'GET',
  credentials: 'include',
})
.then(r => r.json())
.then(data => console.log('Simple:', data))
.catch(err => console.error('Error:', err));
```

### Test from Command Line

```bash
# Using curl (if accessible)
curl http://your-onion-address.onion/api/health/

# Simple check
curl http://your-onion-address.onion/api/health/simple/
```

## Status Meanings

### Healthy
- ✅ Database connected
- ✅ All services available
- ✅ API endpoints working

### Degraded
- ⚠️ Database connected but some services unavailable
- ⚠️ API working but with limitations

### Unhealthy
- ❌ Database not connected
- ❌ Critical services unavailable
- ❌ API not functioning properly

## Monitoring

### Auto-Refresh
The frontend component automatically refreshes every 30 seconds to keep status up-to-date.

### Manual Refresh
Users can click the "Refresh" button to immediately check status.

### Error Handling
If the health check fails (network error, server down), the component shows:
- Status: "UNHEALTHY"
- Error message with details

## Integration

### Add to Other Pages

```typescript
import HealthCheck from '@/components/HealthCheck';

// In your component
<HealthCheck />
```

### Use in Code

```typescript
import { api } from '@/services/api';

// Check health before making API calls
const health = await api.healthCheck();
if (health.status === 'healthy') {
  // Proceed with API calls
} else {
  // Show error or retry
}
```

## Production Considerations

1. **Rate Limiting**: Consider adding rate limiting to health endpoints
2. **Caching**: Health checks can be cached for a few seconds
3. **Monitoring**: Integrate with monitoring services (Prometheus, etc.)
4. **Alerts**: Set up alerts for unhealthy status
5. **Logging**: Log health check failures for debugging

## Security

- ✅ Health endpoints are CORS-enabled
- ✅ No authentication required (public status)
- ✅ No sensitive information exposed
- ✅ Safe to expose publicly

## Files Modified

### Django
- `blog/views.py` - Added `api_health_check()` and `api_health_check_simple()`
- `blog/urls.py` - Added health check routes

### Vite
- `src/services/api.ts` - Added `healthCheck()` and `healthCheckSimple()` methods
- `src/components/HealthCheck.tsx` - New health check component
- `src/pages/BlogPage.tsx` - Added HealthCheck component
- `src/pages/ChatPage.tsx` - Added HealthCheck component

---

**Status:** ✅ Health check system is ready to use!
