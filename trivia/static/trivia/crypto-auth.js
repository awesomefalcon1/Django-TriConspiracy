/**
 * Client-side cryptography for public/private key authentication
 * Uses Web Crypto API for RSA operations
 */

class CryptoAuth {
    constructor() {
        this.privateKey = null;
        this.publicKey = null;
    }

    /**
     * Generate a new RSA key pair using Web Crypto API
     */
    async generateKeyPair() {
        try {
            const keyPair = await window.crypto.subtle.generateKey(
                {
                    name: "RSA-PSS",
                    modulusLength: 2048,
                    publicExponent: new Uint8Array([1, 0, 1]),
                    hash: "SHA-256",
                },
                true,
                ["sign", "verify"]
            );

            // Export keys to PEM format
            const privateKeyPem = await this.exportPrivateKey(keyPair.privateKey);
            const publicKeyPem = await this.exportPublicKey(keyPair.publicKey);

            this.privateKey = keyPair.privateKey;
            this.publicKey = keyPair.publicKey;

            return {
                privateKey: privateKeyPem,
                publicKey: publicKeyPem
            };
        } catch (error) {
            console.error('Error generating key pair:', error);
            throw error;
        }
    }

    /**
     * Import a private key from PEM format
     */
    async importPrivateKey(pem) {
        try {
            // Remove PEM headers and whitespace
            const pemHeader = "-----BEGIN PRIVATE KEY-----";
            const pemFooter = "-----END PRIVATE KEY-----";
            const pemContents = pem
                .replace(pemHeader, "")
                .replace(pemFooter, "")
                .replace(/\s/g, "");
            
            const binaryDer = this.base64ToArrayBuffer(pemContents);
            
            return await window.crypto.subtle.importKey(
                "pkcs8",
                binaryDer,
                {
                    name: "RSA-PSS",
                    hash: "SHA-256",
                },
                true,
                ["sign"]
            );
        } catch (error) {
            console.error('Error importing private key:', error);
            throw error;
        }
    }

    /**
     * Import a public key from PEM format
     */
    async importPublicKey(pem) {
        try {
            const pemHeader = "-----BEGIN PUBLIC KEY-----";
            const pemFooter = "-----END PUBLIC KEY-----";
            const pemContents = pem
                .replace(pemHeader, "")
                .replace(pemFooter, "")
                .replace(/\s/g, "");
            
            const binaryDer = this.base64ToArrayBuffer(pemContents);
            
            return await window.crypto.subtle.importKey(
                "spki",
                binaryDer,
                {
                    name: "RSA-PSS",
                    hash: "SHA-256",
                },
                true,
                ["verify"]
            );
        } catch (error) {
            console.error('Error importing public key:', error);
            throw error;
        }
    }

    /**
     * Sign a message with the private key
     */
    async signMessage(message, privateKeyPem = null) {
        try {
            let key = this.privateKey;
            
            if (privateKeyPem) {
                key = await this.importPrivateKey(privateKeyPem);
            }
            
            if (!key) {
                throw new Error('No private key available');
            }

            const signature = await window.crypto.subtle.sign(
                {
                    name: "RSA-PSS",
                    saltLength: 32,
                },
                key,
                new TextEncoder().encode(message)
            );

            // Convert to base64
            return this.arrayBufferToBase64(signature);
        } catch (error) {
            console.error('Error signing message:', error);
            throw error;
        }
    }

    /**
     * Export private key to PEM format
     */
    async exportPrivateKey(key) {
        const exported = await window.crypto.subtle.exportKey("pkcs8", key);
        const exportedAsBase64 = this.arrayBufferToBase64(exported);
        return `-----BEGIN PRIVATE KEY-----\n${exportedAsBase64.match(/.{1,64}/g).join('\n')}\n-----END PRIVATE KEY-----`;
    }

    /**
     * Export public key to PEM format
     */
    async exportPublicKey(key) {
        const exported = await window.crypto.subtle.exportKey("spki", key);
        const exportedAsBase64 = this.arrayBufferToBase64(exported);
        return `-----BEGIN PUBLIC KEY-----\n${exportedAsBase64.match(/.{1,64}/g).join('\n')}\n-----END PUBLIC KEY-----`;
    }

    /**
     * Convert base64 string to ArrayBuffer
     */
    base64ToArrayBuffer(base64) {
        const binaryString = window.atob(base64);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        return bytes.buffer;
    }

    /**
     * Convert ArrayBuffer to base64 string
     */
    arrayBufferToBase64(buffer) {
        const bytes = new Uint8Array(buffer);
        let binary = '';
        for (let i = 0; i < bytes.byteLength; i++) {
            binary += String.fromCharCode(bytes[i]);
        }
        return window.btoa(binary);
    }
}

// Global instance
const cryptoAuth = new CryptoAuth();
