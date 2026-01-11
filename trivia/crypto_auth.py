"""
Public/Private Key Authentication Utilities
"""
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import base64
import json
import hashlib


def generate_key_pair():
    """
    Generate a new RSA key pair.
    Returns: (private_key_pem, public_key_pem) as strings
    """
    # Generate a 2048-bit RSA key pair
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Serialize private key to PEM format
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode('utf-8')
    
    # Get public key and serialize to PEM format
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    
    return private_key_pem, public_key_pem


def verify_signature(public_key_pem: str, message: str, signature: str) -> bool:
    """
    Verify a signature using a public key.
    Uses PKCS1v15 padding (compatible with jsrsasign's SHA256withRSA).
    
    Args:
        public_key_pem: Public key in PEM format
        message: The original message that was signed
        signature: Base64-encoded signature
    
    Returns:
        True if signature is valid, False otherwise
    """
    try:
        # Load public key
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode('utf-8'),
            backend=default_backend()
        )
        
        # Decode signature from base64
        signature_bytes = base64.b64decode(signature)
        
        # Verify signature using PKCS1v15 (compatible with jsrsasign)
        public_key.verify(
            signature_bytes,
            message.encode('utf-8'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f"Signature verification error: {e}")
        return False


def sign_message(private_key_pem: str, message: str) -> str:
    """
    Sign a message using a private key.
    Uses PKCS1v15 padding (compatible with jsrsasign).
    
    Args:
        private_key_pem: Private key in PEM format
        message: Message to sign
    
    Returns:
        Base64-encoded signature
    """
    # Load private key
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode('utf-8'),
        password=None,
        backend=default_backend()
    )
    
    # Sign the message using PKCS1v15
    signature = private_key.sign(
        message.encode('utf-8'),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    
    # Encode signature to base64
    return base64.b64encode(signature).decode('utf-8')


def get_public_key_fingerprint(public_key_pem: str) -> str:
    """
    Generate a fingerprint from a public key (full SHA256 hash).
    """
    key_hash = hashlib.sha256(public_key_pem.encode('utf-8')).hexdigest()
    return key_hash


def extract_public_key_from_private(private_key_pem: str) -> str:
    """
    Extract the public key from a private key.
    
    Args:
        private_key_pem: Private key in PEM format
    
    Returns:
        Public key in PEM format
    """
    # Load private key
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode('utf-8'),
        password=None,
        backend=default_backend()
    )
    
    # Get public key and serialize to PEM format
    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')
    
    return public_key_pem


def create_post_message(title: str, content: str, timestamp: str) -> str:
    """
    Create a canonical message string for signing a blog post.
    This ensures the signature is tied to the exact content.
    
    Args:
        title: Post title
        content: Post content
        timestamp: ISO format timestamp (string)
    
    Returns:
        Message string to sign
    """
    # Use a canonical format: title|content|timestamp
    # This ensures the signature is tied to the exact content
    return f"{title}|{content}|{timestamp}"
