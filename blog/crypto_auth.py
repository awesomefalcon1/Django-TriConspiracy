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


def encrypt_with_private_key(private_key_pem: str, data: bytes) -> str:
    """
    Encrypt data using a private key.
    In RSA, "encryption" with private key is actually signing, but we use
    the signing operation to create encrypted data that can be verified/decrypted
    with the public key.
    
    Args:
        private_key_pem: Private key in PEM format
        data: Data to encrypt (bytes)
    
    Returns:
        Base64-encoded encrypted/signed data
    """
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import hashes
    
    # Load private key
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode('utf-8'),
        password=None,
        backend=default_backend()
    )
    
    # For RSA, we use signing with the private key (which is the private key operation)
    # This creates data that can be verified with the public key
    # We use PKCS1v15 padding for compatibility
    encrypted = private_key.sign(
        data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    
    return base64.b64encode(encrypted).decode('utf-8')


def decrypt_with_public_key(public_key_pem: str, encrypted_data: str, original_data: bytes) -> bool:
    """
    Verify/decrypt data using a public key.
    Since we used private key signing for "encryption", we verify it with the public key.
    
    Args:
        public_key_pem: Public key in PEM format
        encrypted_data: Base64-encoded encrypted/signed data
        original_data: Original data to verify against
    
    Returns:
        True if verification succeeds (decryption is valid), False otherwise
    """
    from cryptography.hazmat.primitives.asymmetric import padding
    from cryptography.hazmat.primitives import hashes
    
    # Load public key
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode('utf-8'),
        backend=default_backend()
    )
    
    # Decode encrypted/signed data
    encrypted_bytes = base64.b64decode(encrypted_data)
    
    try:
        # Verify the signature (which acts as decryption verification)
        public_key.verify(
            encrypted_bytes,
            original_data,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False


def encrypt_fingerprint_and_hash(private_key_pem: str, fingerprint: str, content: str) -> str:
    """
    Encrypt the fingerprint and content hash using the private key.
    
    Args:
        private_key_pem: Private key in PEM format
        fingerprint: User's fingerprint (SHA256 hash of public key)
        content: Content to hash
    
    Returns:
        Base64-encoded encrypted data containing fingerprint|content_hash
    """
    # Hash the content using SHA256 and encode as base64 (to match client-side)
    content_hash_bytes = hashlib.sha256(content.encode('utf-8')).digest()
    content_hash_b64 = base64.b64encode(content_hash_bytes).decode('utf-8')
    
    # Combine fingerprint and content hash
    data_string = f"{fingerprint}|{content_hash_b64}"
    data_bytes = data_string.encode('utf-8')
    
    # Encrypt with private key
    return encrypt_with_private_key(private_key_pem, data_bytes)


def verify_encrypted_fingerprint_and_hash(public_key_pem: str, encrypted_data: str, fingerprint: str, content: str) -> bool:
    """
    Verify encrypted fingerprint and content hash.
    
    Args:
        public_key_pem: Public key in PEM format
        encrypted_data: Base64-encoded encrypted/signed data
        fingerprint: Expected fingerprint
        content: Content to verify
    
    Returns:
        True if fingerprint and content hash match, False otherwise
    """
    try:
        # Create the expected data string with base64-encoded hash (to match client-side)
        content_hash_bytes = hashlib.sha256(content.encode('utf-8')).digest()
        content_hash_b64 = base64.b64encode(content_hash_bytes).decode('utf-8')
        expected_data_string = f"{fingerprint}|{content_hash_b64}"
        expected_data_bytes = expected_data_string.encode('utf-8')
        
        # Verify the encrypted data matches the expected data
        return decrypt_with_public_key(public_key_pem, encrypted_data, expected_data_bytes)
    except Exception as e:
        print(f"Verification error: {e}")
        return False
