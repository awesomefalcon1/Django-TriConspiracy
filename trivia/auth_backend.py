"""
Custom Authentication Backend for Public Key Authentication
"""
from django.contrib.auth.backends import BaseBackend
from .models import PublicKeyUser
from .crypto_auth import verify_signature, get_public_key_fingerprint
import hashlib


class PublicKeyAuthBackend(BaseBackend):
    """
    Authenticate users using public/private key pairs.
    The client signs a challenge with their private key,
    and we verify it using the stored public key.
    """
    
    def authenticate(self, request, public_key_pem=None, signature=None, challenge=None, **kwargs):
        """
        Authenticate a user using their public key and signature.
        
        Args:
            public_key_pem: The user's public key in PEM format
            signature: Base64-encoded signature of the challenge
            challenge: The challenge message that was signed
        
        Returns:
            PublicKeyUser if authentication succeeds, None otherwise
        """
        if not all([public_key_pem, signature, challenge]):
            return None
        
        # Generate fingerprint from public key
        fingerprint = hashlib.sha256(public_key_pem.encode('utf-8')).hexdigest()
        
        try:
            # Try to find existing user by fingerprint
            user = PublicKeyUser.objects.get(fingerprint=fingerprint)
            
            # Verify the signature
            if not verify_signature(public_key_pem, challenge, signature):
                return None
            
            # Update last login
            user.update_last_login()
            return user
            
        except PublicKeyUser.DoesNotExist:
            # New user - verify signature first, then create
            if not verify_signature(public_key_pem, challenge, signature):
                return None
            
            # Create new user
            user = PublicKeyUser.objects.create_user(public_key_pem=public_key_pem)
            user.fingerprint = fingerprint
            user.save()
            return user
    
    def get_user(self, user_id):
        """Get user by ID"""
        try:
            return PublicKeyUser.objects.get(pk=user_id)
        except PublicKeyUser.DoesNotExist:
            return None
