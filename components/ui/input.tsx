// Input.jsx
import React from 'react';

interface InputProps {
  label?: string;
  id?: string;
  type?: string;
  placeholder?: string;
  value?: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  className?: string;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, id, type, placeholder, value, onChange, className, ...props }, ref) => {
    return (
      <div>
        {label && <label htmlFor={id} className="block text-sm font-medium text-gray-500">{label}</label>}
        <input
          ref={ref}
          type={type}
          id={id}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          className={`mt-1 block w-full bg-gray-800 text-white border border-gray-700 rounded-md py-2 px-3 focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary transition-colors duration-200 ${className}`}
          {...props}
        />
      </div>
    );
  }
);

Input.displayName = 'Input'; // Recommended for debugging purposes

export default Input;