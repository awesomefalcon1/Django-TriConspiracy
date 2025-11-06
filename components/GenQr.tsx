'use client';

import React, { useState } from 'react';
import { QRCodeSVG } from 'qrcode.react';
import { Send } from 'lucide-react';

function QRCodeGenerator() {
    const [qrValue, setQrValue] = useState('https://discord.gg/6GaWZAawUc');

    const handleDownload = () => {
        const svg = document.querySelector('svg');
        if (!svg) return;
        
        const svgData = new XMLSerializer().serializeToString(svg);
        const blob = new Blob([svgData], { type: 'image/svg+xml' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'qrcode.svg';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    };

    const handleShare = async () => {
        if (navigator.share) {
            try {
                await navigator.share({
                    title: 'QR Code',
                    text: 'Check out this QR Code',
                    url: qrValue
                });
            } catch (error) {
                console.error('Error sharing:', error);
            }
        }
    };

    return (
        <section className="max-w-3xl mx-auto text-center">
            <h2 className="text-3xl font-bold mb-6 mt-6 text-white">Or Generate your own</h2>
            <div className="mb-8 flex items-center justify-center gap-2">
                <div className="relative flex-1 max-w-md">
                    <input 
                        type="text"
                        value={qrValue}
                        onChange={(e) => setQrValue(e.target.value)}
                        className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-black bg-white pr-12"
                        placeholder="Enter URL or text for QR code"
                    />
                    {typeof navigator !== 'undefined' && 'share' in navigator && (
                        <button
                            onClick={handleShare}
                            className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-blue-500 transition-colors"
                            aria-label="Share QR Code"
                        >
                            <Send className="h-5 w-5" />
                        </button>
                    )}
                </div>
            </div>
            <div className="bg-white p-8 rounded-lg inline-block">
                <QRCodeSVG 
                    value={qrValue}
                    size={256}
                    level="H"
                />
            </div>
            <div className="mt-4 space-x-4">
                <button
                    onClick={handleDownload}
                    className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
                >
                    Download SVG
                </button>
            </div>
            <p className="mt-4 text-gray-400">
                Scan this code to join our Discord community
            </p>
        </section>
    );
}

export default QRCodeGenerator;
