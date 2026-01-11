# Testing API Endpoints

## Test Register Endpoint

To test if the register endpoint is working, try:

```bash
curl -X POST http://localhost:8000/api/cors/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123","email":"test@example.com"}'
```

Or with the onion address:
```bash
curl -X POST http://your-onion-address.onion/api/cors/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123","email":"test@example.com"}'
```

## Expected Response

Success (201):
```json
{
  "success": true,
  "message": "User created successfully",
  "user": {
    "username": "testuser",
    "user_id": 1
  }
}
```

Error (400):
```json
{
  "error": "Username already exists"
}
```

## Check URL Patterns

The endpoint should be available at:
- `/api/cors/register/` (with trailing slash)

Make sure:
1. Django server is running
2. URL pattern is correct in `blog/urls.py`
3. View function exists in `blog/api_views.py`
4. No URL conflicts in `main/urls.py`
