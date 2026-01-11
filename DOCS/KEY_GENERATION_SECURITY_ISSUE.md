# Key Generation Security Issue

## Current Implementation

### Problem: Server-Side Key Generation

**Current Flow:**
1. User clicks "Create Account (Download Key)" button
2. Backend generates **both** private and public keys on the server
3. Backend returns **only the private key** as a downloadable file
4. Public key is generated but **not provided to the user**
5. User must upload the private key back to login

**Code Location:**
- `blog/views.py` - `generate_keys()` function (lines 88-96)
- `blog/crypto_auth.py` - `generate_key_pair()` function (lines 12-38)

### Security Issues

1. **Private key exists on server** - Even briefly, the private key is generated and handled server-side
2. **Private key transmitted over network** - Sent via HTTP response (even if HTTPS, still a risk)
3. **Server could log/store keys** - No guarantee keys aren't logged or stored
4. **Public key not provided** - User can't verify what public key corresponds to their private key

### Current Code

```python
def generate_keys(request: HttpRequest):
    """Generate a new key pair and return private key as downloadable file"""
    private_key, public_key = generate_key_pair()  # Both generated on server
    
    # Only private key is returned
    response = HttpResponse(private_key, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="private_key.pem"'
    return response
```

## Recommended Solution

### Client-Side Key Generation

Keys should be generated **client-side** using JavaScript Web Crypto API:

1. **User's browser generates keys** - Private key never leaves the browser
2. **User downloads both keys** - Private key and public key
3. **User uploads public key** - Only public key is sent to server
4. **Private key stays local** - Never transmitted to server

### Implementation

The client-side JavaScript (`blog/static/trivia/crypto-auth.js`) already has the capability:

```javascript
async generateKeyPair() {
    const keyPair = await window.crypto.subtle.generateKey(...);
    const privateKeyPem = await this.exportPrivateKey(keyPair.privateKey);
    const publicKeyPem = await this.exportPublicKey(keyPair.publicKey);
    return { privateKey: privateKeyPem, publicKey: publicKeyPem };
}
```

### What Needs to Change

1. **Remove server-side key generation** - Delete or disable `generate_keys()` endpoint
2. **Update login page** - Add client-side key generation button
3. **Provide both keys for download** - Let user download both private and public keys
4. **Registration flow** - User uploads only public key to register

## Current State Summary

- ✅ **Backend generates both keys** - Yes, on the server
- ✅ **User downloads private key** - Yes, as `private_key.pem`
- ❌ **User gets public key** - No, public key is generated but not provided
- ❌ **Security** - Poor, keys generated server-side
- ❌ **Best practice** - Should be client-side generation

## Recommendation

**Immediate action:** Update the system to generate keys client-side and only send the public key to the server for registration.

---

**Status:** ⚠️ Security issue identified - keys should be generated client-side, not server-side.
