'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';

function Header() {
  const [showWIPMessage, setShowWIPMessage] = useState(false);
  
  const handleSignInClick = () => {
    setShowWIPMessage(true);
    setTimeout(() => {
      setShowWIPMessage(false);
    }, 3000);
  };

  return (
    <header className="relative w-full sticky top-0 bg-gray-900 text-white shadow-md z-50">
            <nav className="absolute top-0 left-0 p-6">
        
          <div className="flex items-center">
            <Image
              src="/logo-header.png"
              alt="DKK Logo"
              width={32}
              height={32}
              className="mr-2"
            />
           </div>
      </nav>
      <nav className="absolute top-0 right-0 p-6">
        
        <div className="flex items-center gap-4">
          <Link href="/" className="text-white hover:text-primary">Home</Link>
          <Link href="/docs" className="text-white hover:text-primary">Docs</Link>
          <Link href="/guide" className="text-white hover:text-primary">Guide</Link>
          <Link href="/sign-in" className="text-white hover:text-primary">Sign In</Link>
        </div>
      </nav>
    </header>
  );
}

export default Header;
