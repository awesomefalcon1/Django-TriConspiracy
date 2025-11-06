// Label.jsx
import React from 'react';

interface LabelProps {
  htmlFor: string;
  children: React.ReactNode;
  className?: string;
}

const Label = ({ htmlFor, children, className, ...props }: LabelProps) => {
  return (
    <label htmlFor={htmlFor} className={`block text-sm font-medium text-gray-500 ${className}`} {...props}>
      {children}
    </label>
  );
};

export default Label;