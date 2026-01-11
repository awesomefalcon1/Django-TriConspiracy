# TriConspiracy - Security & Usage Documentation

## Security Evaluation & Improvements

### Key Generation Security ✅ FIXED

**Previous Issue:** Keys were generated server-side, which is a security risk because:
- The server could potentially log or store private keys
- Users had to trust the server not to compromise their keys
- Keys were transmitted over the network

**Current Implementation:** 
- ✅ Keys are now generated **client-side** using the Web Crypto API
- ✅ Private keys are **never sent to the server**
- ✅ Keys are downloaded as files for secure storage
- ✅ Private keys are stored in browser localStorage (temporary, for convenience)
- ✅ Users can upload their private key file when needed

### Onion Service Security

**Question: Is onion service HTTPS? Is it secured?**

**Answer:** 
- Onion services use **HTTP** (not HTTPS) at the application layer
- However, **Tor provides encryption at the network layer** through its circuit encryption
- The connection is **secured** through:
  1. **End-to-end encryption** via Tor's multi-hop circuit
  2. **Hidden service encryption** - traffic is encrypted between the client and the hidden service
  3. **No need for TLS/HTTPS certificates** - Tor's encryption replaces this need

**Security Properties:**
- ✅ Traffic is encrypted between your browser and the hidden service
- ✅ Your IP address is hidden from the server
- ✅ The server's IP address is hidden from you
- ✅ Traffic analysis is difficult due to Tor's circuit design
- ⚠️ Application-layer data is still HTTP (but encrypted by Tor)
- ⚠️ No certificate validation (but not needed with Tor's encryption)

**Best Practices:**
- Always use Tor Browser when accessing .onion addresses
- The connection is secure even without HTTPS certificates
- For additional security, you can use end-to-end encryption (which this app provides via public key cryptography)

### CORS Configuration

The backend now supports CORS for GitHub/GitLab Pages:
- Configured to allow requests from `*.github.io` and `*.gitlab.io`
- Credentials (cookies) are allowed for session management
- All necessary HTTP methods and headers are permitted

**To configure your specific domain:**
1. Edit `main/settings.py`
2. Add your specific GitHub/GitLab Pages URL to `CORS_ALLOWED_ORIGINS`
3. Example: `"https://yourusername.github.io"`

## Diffie-Hellman Key Exchange

**What is Diffie-Hellman Key Exchange?**

Diffie-Hellman (DH) is a cryptographic protocol that allows two parties to establish a shared secret key over an insecure channel, even if they've never communicated before.

**How Does it Work?**

1. **Setup:** Both parties agree on:
   - A large prime number `p` (modulus)
   - A generator `g` (base)

2. **Key Generation:**
   - Alice generates a private key `a` and computes `A = g^a mod p` (public key)
   - Bob generates a private key `b` and computes `B = g^b mod p` (public key)

3. **Key Exchange:**
   - Alice sends `A` to Bob
   - Bob sends `B` to Alice

4. **Shared Secret:**
   - Alice computes: `s = B^a mod p = (g^b)^a mod p = g^(ab) mod p`
   - Bob computes: `s = A^b mod p = (g^a)^b mod p = g^(ab) mod p`
   - Both arrive at the same shared secret `g^(ab) mod p`

5. **Security:**
   - An eavesdropper sees `A`, `B`, `g`, and `p`
   - But computing `g^(ab) mod p` from these values is computationally infeasible (discrete logarithm problem)

**Use Cases:**
- TLS/SSL handshakes
- VPN protocols
- Secure messaging apps
- Key agreement in cryptographic protocols

**Note:** This application uses **RSA public key cryptography** (not Diffie-Hellman) for authentication. RSA is used for:
- Digital signatures (proving identity)
- Key pair generation (public/private keys)
- Challenge-response authentication

## Architecture

### Frontend (GitHub/GitLab Pages)
- Static HTML/JavaScript files
- Client-side key generation
- CORS-based API communication
- No server-side code

### Backend (Django on Tor Hidden Service)
- RESTful API endpoints
- Public key authentication
- Blog post management
- Chat messaging
- CORS-enabled for frontend access

## Usage Instructions

### 1. Setup Backend (Django)

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations (after adding ChatMessage model)
python manage.py makemigrations
python manage.py migrate

# Run server (configured for Tor hidden service)
python manage.py runserver 0.0.0.0:8000
```

### 2. Configure CORS

Edit `main/settings.py` and add your GitHub/GitLab Pages URL:
```python
CORS_ALLOWED_ORIGINS = [
    "https://yourusername.github.io",
    # ... other origins
]
```

### 3. Deploy Frontend

1. Copy `frontend_index.html` to `index.html` in your GitHub/GitLab Pages repository
2. Copy `blog/static/trivia/crypto-auth.js` to your repository
3. Update the backend URL in the frontend (or let users configure it)

### 4. User Workflow

1. **Generate Keys:**
   - Click "Generate & Download Keys"
   - Save `private_key.pem` and `public_key.pem` securely
   - Keys are automatically stored in browser localStorage

2. **Configure Backend:**
   - Enter your Django backend's .onion address
   - The URL is saved in localStorage

3. **Register/Login:**
   - Click "Register/Login"
   - Your public key is sent to the server
   - You sign a challenge with your private key
   - Server verifies your signature

4. **Use the App:**
   - Create blog posts (requires authentication)
   - Send chat messages (can be anonymous)
   - View posts and messages

## API Endpoints

### Authentication
- `GET /api/cors/challenge/` - Get authentication challenge
- `POST /api/cors/register/` - Register with public key
- `POST /api/cors/login/` - Authenticate with signature

### Blog
- `GET /api/cors/posts/` - Get published posts
- `POST /api/cors/posts/create/` - Create new post (requires auth)

### Chat
- `GET /api/cors/chat/messages/` - Get chat messages
- `POST /api/cors/chat/send/` - Send message (optional auth)

## Security Features

1. **Client-Side Key Generation** - Keys never touch the server
2. **Public Key Authentication** - No passwords, only cryptographic proof
3. **Challenge-Response** - Prevents replay attacks
4. **Tor Encryption** - Network-layer security
5. **CORS Protection** - Only allowed origins can access API
6. **Signature Verification** - Supports both RSA-PSS and PKCS1v15

## Security Considerations

### ✅ Good Practices Implemented
- Private keys never sent to server
- Client-side key generation
- Cryptographic authentication
- Tor network encryption
- CORS protection

### ⚠️ Considerations
- Private keys stored in localStorage (temporary, for convenience)
- Consider using IndexedDB or a more secure storage mechanism
- Implement key encryption at rest (future enhancement)
- Consider implementing key derivation for additional security
- Rate limiting on API endpoints (recommended for production)

## Future Enhancements

1. **Web Store Solution** - Secure private key storage (as mentioned)
2. **End-to-End Encryption** - Encrypt chat messages with recipient's public key
3. **Key Rotation** - Allow users to rotate their keys
4. **Multi-Device Support** - Sync keys across devices securely
5. **Backup & Recovery** - Secure key backup mechanisms

## Troubleshooting

### CORS Errors
- Ensure your frontend URL is in `CORS_ALLOWED_ORIGINS`
- Check that `CORS_ALLOW_CREDENTIALS = True`
- Verify backend is accessible from frontend

### Authentication Failures
- Ensure private key is correctly loaded
- Check that backend supports RSA-PSS signatures
- Verify challenge is being signed correctly

### Connection Issues
- Verify Tor hidden service is running
- Check .onion address is correct
- Ensure backend is accessible via Tor

## License & Disclaimer

This software is provided for educational and research purposes. Use at your own risk. Always review security implementations before deploying to production.
