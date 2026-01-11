# Netlify + Django API Connection Setup

## Quick Setup Guide

### 1. Configure Django CORS for Netlify

The Django backend is already configured to accept requests from Netlify. The CORS settings in `main/settings.py` include:
- `https://*.netlify.app`
- `https://*.netlify.com`
- Regex patterns for all Netlify subdomains

### 2. Set Environment Variable in Netlify

1. Go to your Netlify site dashboard
2. Navigate to **Site settings** > **Build & deploy** > **Environment variables**
3. Add a new variable:
   - **Key:** `VITE_API_BASE_URL`
   - **Value:** Your Django backend URL
     - For Tor: `http://your-onion-address.onion`
     - For regular server: `https://your-django-server.com`
     - For local testing: `http://localhost:8000`

### 3. Deploy to Netlify

The `netlify.toml` file is already configured. Just:

1. Push your code to GitHub/GitLab
2. Connect the repository to Netlify
3. Netlify will automatically:
   - Run `npm run build`
   - Deploy from the `dist` folder
   - Use the environment variable you set

### 4. Test the Connection

After deployment, test the API connection:

1. Open your Netlify site
2. Open browser DevTools (F12)
3. Go to Console tab
4. Try using the Blog or Chat features
5. Check Network tab for API calls

## API Endpoints Used

The frontend uses these Django endpoints:

### Chat
- `GET /api/dh/chat/messages/` - Get chat messages
- `POST /api/cors/chat/send/` - Send chat message

### Blog
- `GET /api/dh/blog/posts/` - Get blog posts
- `POST /api/cors/posts/create/` - Create blog post

## Troubleshooting

### CORS Errors

If you see CORS errors in the browser console:

1. **Check Django CORS settings:**
   ```python
   # In main/settings.py
   CORS_ALLOWED_ORIGINS = [
       "https://your-app.netlify.app",  # Add your specific Netlify URL
       # ...
   ]
   ```

2. **Check environment variable:**
   - Make sure `VITE_API_BASE_URL` is set in Netlify
   - Rebuild the site after adding the variable

3. **Check Django server:**
   - Ensure Django is running and accessible
   - Check that CORS middleware is enabled

### API Connection Errors

1. **Check API URL:**
   - Verify `VITE_API_BASE_URL` is correct
   - Test the API URL directly in browser/Postman

2. **Check Django logs:**
   - Look for errors in Django console
   - Check for 404/500 errors

3. **Network issues:**
   - If using Tor, ensure Tor is running
   - Check firewall settings

### Build Errors

1. **Missing dependencies:**
   ```bash
   npm install
   ```

2. **TypeScript errors:**
   - Check `tsconfig.json`
   - Fix any type errors

3. **Environment variable not found:**
   - Make sure variable is set in Netlify dashboard
   - Variable name must start with `VITE_`

## Current Implementation

The frontend currently uses:
- **Simplified API service** (`src/services/api.ts`)
- **CORS endpoints** for sending messages (no encryption required)
- **DH endpoints** for reading messages (backend handles encryption)

This works immediately without additional libraries. For full DH encryption on the client side, you'll need to add a DH library later.

## Next Steps (Optional)

To add full client-side DH encryption:

1. Install DH library:
   ```bash
   npm install node-forge
   ```

2. Update `src/services/api.ts` to use DH encryption
3. Update backend to handle encrypted messages from client

For now, the current setup works and connects Netlify to Django!
