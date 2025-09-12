// Ensure the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Configuration
    const HEADER_HEIGHT = 100; // px
    const HEADER_SELECTOR = 'header, .navbar, nav, .bg-\\[\\#014903\\]';
    const LOGO_SELECTOR = '.header-logo, .navbar-brand img, .fmwa-logo-stretch, img[alt*="Logo"], img[alt*="logo"]';
    
    // Function to apply header fixes
    function fixHeader() {
        // Get all header elements
        const headers = document.querySelectorAll(HEADER_SELECTOR);
        const logos = document.querySelectorAll(LOGO_SELECTOR);
        
        // Apply styles to headers
        headers.forEach(header => {
            Object.assign(header.style, {
                'position': 'fixed',
                'top': '0',
                'left': '0',
                'right': '0',
                'z-index': '9999',
                'margin': '0',
                'padding': '0',
                'background-color': '#014903',
                'min-height': `${HEADER_HEIGHT}px`,
                'height': `${HEADER_HEIGHT}px`,
                'max-height': `${HEADER_HEIGHT}px`,
                'box-shadow': '0 2px 4px rgba(0,0,0,0.1)',
                'display': 'flex',
                'align-items': 'center'
            });
        });
        
        // Apply styles to logos
        logos.forEach(logo => {
            Object.assign(logo.style, {
                'height': `${HEADER_HEIGHT}px`,
                'width': 'auto',
                'max-height': `${HEADER_HEIGHT}px`,
                'object-fit': 'contain',
                'margin': '0',
                'padding': '0',
                'display': 'block'
            });
        });
        
        // Ensure body has proper padding
        document.body.style.paddingTop = `${HEADER_HEIGHT}px`;
        
        // Add a class to the body when header is fixed
        document.body.classList.add('header-fixed');
    }
    
    // Run on load
    fixHeader();
    
    // Re-apply on window resize
    window.addEventListener('resize', fixHeader);
    
    // Re-apply when dynamic content loads
    if (typeof MutationObserver !== 'undefined') {
        const observer = new MutationObserver(fixHeader);
        observer.observe(document.body, { 
            childList: true, 
            subtree: true,
            attributes: true,
            attributeFilter: ['style', 'class']
        });
    }
});
