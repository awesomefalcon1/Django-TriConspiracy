import React from 'react';
import Image from 'next/image';

function Footer() {
  return (
    <footer className="bg-gray-900">
      <div className="container mx-auto px-6 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center">
            <Image
              src="/logo-header.png"
              alt="DKK Logo"
              width={32}
              height={32}
              className="mr-2"
            />
            <span className="text-white text-sm">© 2024 Duo Keyboard Koalition</span>
          </div>
          <div className="flex gap-4">
            <a href="https://github.com/your-github-org" target="_blank" rel="noopener noreferrer" className="text-white hover:text-primary text-sm">GitHub</a>
            <a href="https://twitter.com/your-twitter-handle" target="_blank" rel="noopener noreferrer" className="text-white hover:text-primary text-sm">Twitter</a>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
