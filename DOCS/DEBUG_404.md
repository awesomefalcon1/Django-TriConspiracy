# Debugging 404 Error on Register Endpoint

## Issue
Getting `HTTP 404: Not Found` when trying to sign up.

## Possible Causes

1. **URL Routing Order**: The `path('api/', api_root, ...)` in `main/urls.py` might be interfering
   - **Fix**: Reordered URLs so `blog.urls` is included before `api_root`

2. **Trailing Slash**: Django is sensitive to trailing slashes
   - **Check**: Make sure URL pattern has trailing slash: `api/cors/register/`
   - **Check**: Make sure frontend calls it with trailing slash: `/api/cors/register/`

3. **API Base URL**: Frontend might not be pointing to correct server
   - **Check**: Verify `VITE_API_BASE_URL` is set correctly
   - **Check**: Check browser console for actual URL being called

4. **CORS Preflight**: OPTIONS request might be failing
   - **Check**: Look in browser Network tab for OPTIONS request
   - **Fix**: Ensure CORS is properly configured

## Testing Steps

1. **Test with curl**:
```bash
curl -X POST http://localhost:8000/api/cors/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123","email":"test@test.com"}'
```

2. **Check Django logs**:
   - Look for the actual request path in Django console
   - Check if URL pattern is matching

3. **Check browser Network tab**:
   - See what URL is actually being called
   - Check if it's a 404 or CORS error
   - Check request headers

4. **Verify URL patterns**:
```python
# In Django shell:
python manage.py shell
>>> from django.urls import reverse
>>> reverse('blog:api_cors_register')
# Should return: '/api/cors/register/'
```

## Current URL Configuration

- `main/urls.py`: Includes `blog.urls` at root `''`
- `blog/urls.py`: Has pattern `'api/cors/register/'`
- Full URL: `/api/cors/register/`

## Next Steps

1. Restart Django server after URL changes
2. Clear browser cache
3. Check browser console for actual error
4. Test with curl to verify endpoint works
5. Check Django logs for incoming requests
