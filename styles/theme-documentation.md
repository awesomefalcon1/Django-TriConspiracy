# Website Styling Documentation

## Colors

- **Primary**: #FFA500 (Orange)
- **Secondary**: #4A4A4A (Dark Gray)
- **Background**: Black
- **Text**: White
- **Footer background**: Gray-900 (Tailwind dark gray)
- **Links hover**: Primary color (Orange)

## Layout

- The site uses Tailwind CSS for styling
- Dark theme with black background and white text
- Responsive design with container classes

## Header

- Banner image with responsive height (200px on mobile, 300px on larger screens)
- Navigation links positioned absolutely at the top right
- Links change to primary color (orange) on hover

## Footer

- Dark gray background (bg-gray-900)
- Contains logo, copyright text, and social links
- Social links change to primary color (orange) on hover

## CSS Classes

### Navigation Links
```css
.nav-link {
  @apply text-white hover:text-primary transition-colors duration-200;
}
```

### Buttons
```css
.btn-primary {
  @apply bg-primary text-white px-4 py-2 rounded hover:bg-opacity-90 transition-colors;
}

.btn-secondary {
  @apply bg-secondary text-white px-4 py-2 rounded hover:bg-opacity-90 transition-colors;
}
```
