// Image Lazy Loading Script
// Automatically adds loading="lazy" to images below the fold

document.addEventListener('DOMContentLoaded', function() {
  const images = document.querySelectorAll('img:not([loading])');
  images.forEach(function(img) {
    img.setAttribute('loading', 'lazy');
  });
});
