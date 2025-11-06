import React from 'react';
import { QRCodeSVG } from 'qrcode.react';

interface QRCodeProps {
  value?: string;
  title?: string;
  description?: string;
}

function QRCode({ 
  value = "https://discord.gg/6GaWZAawUc", 
  title = "Scan Our QR Code", 
  description = "Scan this code to join our Discord community" 
}: QRCodeProps) {
  return (
    <section className="max-w-3xl mx-auto text-center">
      <h2 className="text-3xl font-bold mb-6 mt-6 text-white">{title}</h2>
      <div className="bg-white p-8 rounded-lg inline-block">
        <QRCodeSVG 
          value={value}
          size={256}
          level="H"
        />
      </div>
      <p className="mt-4 text-gray-400">
        {description}
      </p>
      <div className="mt-6">
        <a 
          href="https://discord.gg/6GaWZAawUc" 
          target="_blank" 
          rel="noopener noreferrer" 
          className="inline-flex items-center justify-center px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-lg transition-colors duration-200"
        >
          Join Our Discord
        </a>
      </div>
    </section>
  );
}

export default QRCode;
