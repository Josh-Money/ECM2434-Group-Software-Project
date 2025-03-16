document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const isPrivacyPage = currentPath === '/privacy-policy/';
    
    const logo = document.getElementById('footer-logo')
    const earthMascot = document.getElementById('earthMascot');
    const termsBtn = document.getElementById('termsBtn');
    
    if (isPrivacyPage) {
        // On privacy policy page: hide mascot and terms button
        earthMascot.style.display = 'none';
        termsBtn.style.display = 'none';
    } else {
        // On all other pages: hide logo
        console.log(logo);
        logo.style.opacity = 0;
    }
});